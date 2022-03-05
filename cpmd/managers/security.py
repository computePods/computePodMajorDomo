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

  def addedHostPublicKey(self, hostPublicKey) :
    """Add a host's public key"""

    hostName = hostPublicKey.host
    hostPublicKeys = self.securityData['hostPublicKeys']
    hostPublicKeys[hostName] = hostPublicKey
    return True

  def removedHostPublicKey(self, hostPublicKey) :
    """Remove a host's public key"""

    hostName = hostPublicKey.host
    hostPublicKeys = self.securityData['hostPublicKeys']
    if hostName in hostPublicKeys :
      del hostPublicKeys[hostName]
    if hostName not in hostPublicKeys :
      return True
    return False
