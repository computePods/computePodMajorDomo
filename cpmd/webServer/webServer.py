from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

#import aiofiles
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
import os
import yaml

#import cpinterfaces.python.AllFastApiExamples
import cpinterfaces.python.AllFastApiRoutes
#import cpmd.webServer.publish
import cpmd.webServer.projects

class WebServer :

  #addPublishInterface = cpmd.webServer.publish.addPublishInterface

  def __init__(self, config, managers) :
    self.app = FastAPI()
    self.config = config
    self.managers = managers

    #cpinterfaces.python.AllFastApiExamples.addAllExamples(self.app)
    cpinterfaces.python.AllFastApiRoutes.addAllInterface(self.app)
    #self.addPublishInterface()
    cpmd.webServer.projects.implementProjectInterfaces(self)

    #self.app.mount("/clientApp", StaticFiles(directory="clientApp"), name='clientApp')

    #@self.app.get("/", response_class=HTMLResponse)
    #async def read_root():
      #print("webServer cwd: {}".format(os.getcwd()))
      #async with aiofiles.open('clientApp/mcv.html', mode='r') as f:
        #mcvHtml = await f.read()
        #return mcvHtml

    if 'verbose' in self.config and self.config['verbose'] :
      print("----------------------------------------------------------")
      for aRoute in self.app.routes :
        print(f"route path: {aRoute.path} name: {aRoute.name}")
      print("----------------------------------------------------------")

  async def runApp(self, config, wsShutDown) :

  # We will listen for NATS reload events (or changes to files in
  # directories we are using) and then use the graceful shutdown to
  # shutdown and restart the server.
  #
  # https://pgjones.gitlab.io/hypercorn/how_to_guides/api_usage.html#graceful-shutdown

    wsConfig = Config()
    bindings = []
    reload   = False
    for aSocket in config['webServer']['sockets'] :
      binding = None
      if 'path' in aSocket :
        aPath = os.path.expanduser(aSocket['path'])
        aBinding = "unix:{}".format(aPath)
        wsConfig.umask = 0o077
        oldMask = os.umask(0o077)
        os.makedirs(os.path.dirname(aPath), exist_ok=True)
        os.umask(oldMask)
        print("webServer binding to: [{}]".format(aBinding))
      elif 'host' in aSocket and 'port' in aSocket :
        aBinding = "{}:{}".format(aSocket['host'], aSocket['port'])
        print("webServer binding to: [https://{}]".format(aBinding))
      if aBinding is not None :
        bindings.append(aBinding)
      if 'reload' in aSocket : reload = aSocket['reload']
    wsConfig.bind = bindings
    wsConfig.use_reload = reload
    wsConfig.accesslog  = '-'
    await serve(self.app, wsConfig, shutdown_trigger=wsShutDown.wait)

"""
Use os.getloadavg and os.cpu_count to get system information
"""
