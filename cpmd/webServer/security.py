"""Add the projects interface."""

import os
import yaml

from cpinterfaces.python.hostPublicKey import HostPublicKey

import logging
logger = logging.getLogger("majorDomo")

def implementSecurityInterfaces(self) :

  @self.app.get_security_rsyncPublicKey
  async def get_security_rsyncPublicKey_impl() :
    rsyncPublicKey = "unknown"
    if 'rsyncPublicKey' in self.config :
      rsyncPublicKeyFile = self.config['rsyncPublicKey']
      if os.path.isfile(rsyncPublicKeyFile) and \
        os.access(rsyncPublicKeyFile, os.R_OK) :
        with open(self.config['rsyncPublicKey'], 'r') as rpkf :
          rsyncPublicKey = rpkf.read()

    return rsyncPublicKey.strip()

  @self.app.post_security_addHostPublicKey
  async def post_security_addHostPublicKey_impl( hostPublicKey: HostPublicKey) :
    logger.info("addHostPublicKey: {}".format(hostPublicKey))
    result = "Not added"
    if await self.managers.security.addedHostPublicKey(hostPublicKey) :
      result = "Added"
    return {
      'result' : result,
      'host'   : hostPublicKey.host
    }

  @self.app.post_security_removeHostPublicKey
  async def post_security_removeHostPublicKey_impl( hostPublicKey: HostPublicKey) :
    result = "Not removed"
    if await self.managers.security.removedHostPublicKey(hostPublicKey) :
      result = "Removed"
    return {
      'result' : result,
      'host'   : hostPublicKey.host
    }
