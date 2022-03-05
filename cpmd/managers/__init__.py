# We create the collection of managers on behalf of the MajorDomo

from types import SimpleNamespace

from .projects import ProjectsManager
from .security import SecurityManager

def startManagers(toolName, config, natsClient) :

#  projectDirs = []
#  if 'projectDirs' in config :
#    projectDirs = config['projectDirs']

  #projects = ProjectsManager(toolName, projectDirs, natsClient)
  projects = ProjectsManager(toolName, natsClient)
  security = SecurityManager(toolName, natsClient)

  return SimpleNamespace(
    toolName=toolName,
    natsClient=natsClient,
    projects=projects,
    security=security
  )