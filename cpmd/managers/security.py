# The ComputePods Security Manager component

import os
import yaml

import logging
logger = logging.getLogger("majorDomo")

class SecurityManager :
  """The ComputePods SecurityManager loads, parse and maintains the security
  details for a user's use of a federation of ComputePods."""

  def __init__(self, toolName, natsClient) :
    self.toolName    = toolName
    self.nc          = natsClient
    self.securityData = {
      'hostPublicKeys' : {}
    }

    @natsClient.subscribe("security.getHostPublicKeys")
    async def getHostPublicKeys(subject, data) :
      await self.sendHostPublicKeys()

  async def sendHostPublicKeys(self) :
      hostPublicKeys = self.securityData['hostPublicKeys']
      await self.nc.sendMessage(
        "security.hostPublicKeys",
        hostPublicKeys,
        0.1
      )

  async def addedHostPublicKey(self, hostPublicKey) :
    """Add a host's public key"""

    hostName = hostPublicKey.host
    hostPublicKeys = self.securityData['hostPublicKeys']
    hostPublicKeys[hostName] = {
      'host'      : hostPublicKey.host,
      'publicKey' : hostPublicKey.publicKey
    }
    await self.sendHostPublicKeys()
    return True

  async def removedHostPublicKey(self, hostPublicKey) :
    """Remove a host's public key"""

    removed = False
    hostName = hostPublicKey.host
    hostPublicKeys = self.securityData['hostPublicKeys']
    if hostName in hostPublicKeys :
      del hostPublicKeys[hostName]
    if hostName not in hostPublicKeys :
      removed = True

    await self.sendHostPublicKeys()
    return removed
