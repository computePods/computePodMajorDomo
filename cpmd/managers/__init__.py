# We create the collection of managers on behalf of the MajorDomo

from types import SimpleNamespace

from .projects import ProjectsManager

def startManagers(toolName, config, natsClient) :

#  projectDirs = []
#  if 'projectDirs' in config :
#    projectDirs = config['projectDirs']

  #projects = ProjectsManager(toolName, projectDirs, natsClient)
  projects = ProjectsManager(toolName, natsClient)

  return SimpleNamespace(
    toolName=toolName,
    natsClient=natsClient,
    projects=projects,
  )