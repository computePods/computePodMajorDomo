""" Load and normalize the cpmd configuration """

import argparse
import os
import yaml

import cputils.yamlLoader

def parseCliArgs() :

  argparser = argparse.ArgumentParser(
    description="A tool, used by a user, to start and monitor one or more tasks inside a federation of ComputePods."
  )
  argparser.add_argument("-c", "--config", action='append',
    default=[], help="overlay configuration from file"
  )
  argparser.add_argument("-v", "--verbose", default=False,
    action=argparse.BooleanOptionalAction,
    help="show the loaded configuration"
  )
  argparser.add_argument("-d", "--debug", default=False,
    action=argparse.BooleanOptionalAction,
    help="provide debugging output"
  )
  argparser.add_argument("-p", "--project", action='append',
    default=[], help="Add a project directory to manage"
  )
  argparser.add_argument("-r", "--reload", default=False,
    action="store_true",
    help="Reload the webserver if any application files change")

  return argparser.parse_args()

def loadConfig(cliArgs) :

  """

  Load the configuration by merging any `cpmdConfig.yaml` found in the
  current working directory, and then any other configuration files
  specified on the command line.

  Then perform the following normalisation:

  """
  print("Hello from loadConfig")

  config = {
    'verbose' : False,
    'debug'   : False,
    'natsServer' : {
      'host' : '0.0.0.0',
      'port' : 4222
    },
    'webServer' : {
      'sockets' : [
      ]
    },
    'projectDirs' : [ ]
  }

  if cliArgs.verbose :
    config['verbose'] = cliArgs.verbose

  if cliArgs.debug :
    config['debug'] = cliArgs.debug

  unLoadedConfig = cliArgs.config.copy()
  unLoadedConfig.insert(0,'cpmdConfig.yaml')
  print(yaml.dump(unLoadedConfig))
  while 0 < len(unLoadedConfig) :
    aConfigPath = unLoadedConfig[0]
    del unLoadedConfig[0]
    if os.path.exists(aConfigPath) :
      try :
        cputils.yamlLoader.loadYamlFile(config, aConfigPath)
        if 'include' in config :
          unLoadedConfig.extend(config['include'])
          del config['include']
      except Exception as err :
        print("Could not load configuration from [{}]".format(aConfigPath))
        print(err)

  if cliArgs.project :
    config['projectDirs'] = cliArgs.project

  if 'webServer' not in config :
    config['webServer'] = { }
  if 'sockets' not in config['webServer'] :
    config['webServer']['sockets'] = []

  if config['verbose'] :
    print("--------------------------------------------------------------")
    print(yaml.dump(config))
    print("--------------------------------------------------------------")

  return config
