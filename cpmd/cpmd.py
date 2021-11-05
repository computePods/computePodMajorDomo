import argparse
import asyncio
import logging
import signal
import sys
import traceback

from cpmd.webServer import WebServer
from cpmd.loadConfiguration import parseCliArgs, loadConfig
from cpmd.managers import startManagers


#import cputils.recursivewatch
from   cputils.natsClient import NatsClient

async def runTasks(config, wsShutDown) :

  natsClient = NatsClient("majorDomo", 10)
  host = "127.0.0.1"
  port = 4222
  if 'natsServer' in config :
    natsServerConfig = config['natsServer']
    if 'host' in natsServerConfig : host = natsServerConfig['host']
    if 'port' in natsServerConfig : port = natsServerConfig['port']
  natsServerUrl = f"nats://{host}:{port}"
  print(f"connecting to nats server: [{natsServerUrl}]")
  await natsClient.connectToServers([ natsServerUrl ])

  managers = startManagers("majorDomo", config, natsClient)

  ws = WebServer(config, managers)

  try:
    await asyncio.gather(
      natsClient.heartBeat(),
      ws.runApp(config, wsShutDown),
    )
  finally:
    await natsClient.closeConnection()


def cpmd() :
  cliArgs = parseCliArgs()

  if cliArgs.debug :
    logging.basicConfig(level=logging.DEBUG)
  else :
    logging.basicConfig(level=logging.WARNING)
  logger = logging.getLogger("majorDomo")

  #logging.basicConfig(filename='majorDomo.log', encoding='utf-8', level=logging.DEBUG)
  #logging.basicConfig(level=logging.INFO)

  logger.info("ComputePods MajorDomo starting")

  config = loadConfig(cliArgs)

  loop = asyncio.get_event_loop()
  wsShutDown = asyncio.Event()

  def signalHandler(signum) :
    """
    Handle an OS system signal by stopping the debouncing tasks

    """
    print("")
    print("Shutting down...")
    logger.info("SignalHandler: Caught signal {}".format(signum))
    wsShutDown.set()
    loop.stop()

  loop.set_debug(cliArgs.verbose)
  loop.add_signal_handler(signal.SIGTERM, signalHandler, "SIGTERM")
  loop.add_signal_handler(signal.SIGHUP,  signalHandler, "SIGHUP")
  loop.add_signal_handler(signal.SIGINT,  signalHandler, "SIGINT")
  loop.create_task(runTasks(config, wsShutDown))
  loop.run_forever()

  print("\ndone!")
