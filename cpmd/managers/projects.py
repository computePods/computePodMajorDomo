# The ComputePods Projects Manager component

import os
import yaml

import cputils.yamlLoader

class ProjectsManager :
  """The ComputePods ProjectsManager loads, parse and maintains the project
  details for a user's use of a federation of ComputePods."""

  def __init__(self, toolName, projectDirs, natsClient) :
    self.toolName    = toolName
    self.nc          = natsClient
    self.projectDirs = projectDirs
    self.projectData = {
      'projects' : {}
    }

    if len(projectDirs) < 1 :
      print("\nWARNING: No project directories provided!\n")

    try :
      for aProjectDir in projectDirs :
        projectDir = os.path.abspath(os.path.expanduser(aProjectDir))
        self.loadProjectsFrom(projectDir)
    except Exception as err :
      print(f"Could not load the [{aProjectDir}] project")
      print(repr(err))
      print("")

  def loadProjectsFrom(self, aProjectDir) :
    """Load project from YAML files in the directory provided"""

    def addProjectDir(newYamlData) :
      if 'projects' in newYamlData :
        for projectName, projectData in newYamlData['projects'].items() :
          projectData['path'] = aProjectDir

    newProjectData = cputils.yamlLoader.loadYamlFrom(
      self.projectData, aProjectDir, [ '.PYML'],
      callBack=addProjectDir
    )

  async def registerProjects(self) :
    theProjects = self.projectData['projects']
    for aProject, theProject in theProjects.items() :
      await self.nc.sendMessage(
      "register.projects",
      {
        "chefName"    : self.chefName,
        "projectName" : aProject,
        "theProject"  : theProject
      },
        0.1
      )

