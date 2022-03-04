"""Add the projects interface."""

import os
import yaml

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
