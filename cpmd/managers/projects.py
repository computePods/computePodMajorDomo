# The ComputePods Projects Manager component

import os
import yaml

import logging
logger = logging.getLogger("majorDomo")

class ProjectsManager :
  """The ComputePods ProjectsManager loads, parse and maintains the project
  details for a user's use of a federation of ComputePods."""

  def __init__(self, toolName, natsClient) :
    self.toolName    = toolName
    self.nc          = natsClient
    self.projectData = {
      'projects' : {}
    }

  def listProjects(self) :
    """List known projects"""

    projects = self.projectData['projects']
    logger.debug(type(projects))
    logger.debug(yaml.dump(projects))
    projectsDict = {}
    for aProject, projectDetails in projects.items() :
      projectsDict[aProject] = projectDetails.projectDir
    return projectsDict

  def addedProject(self, projectDetails) :
    """Add the project definition"""

    projectName = projectDetails.projectName

    projects = self.projectData['projects']
    if projectName not in projects :
      projects[projectName] = projectDetails
      return True
    return False

  def updatedProject(self, projectDetails) :
    """Update the project definition"""

    projectName = projectDetails.projectName
    projects = self.projectData['projects']
    if projectName in projects :
      projects[projectName] = projectDetails
      return True
    return False

  def removedProject(self, projectDetails) :
    """Remove the project definition"""

    projectName = projectDetails.projectName
    projects = self.projectData['projects']
    if projectName in projects :
      del projects[projectName]
    if projectName not in projects :
      return True
    return False

#  async def registerProjects(self) :
#    theProjects = self.projectData['projects']
#    for aProject, theProject in theProjects.items() :
#      await self.nc.sendMessage(
#      "register.projects",
#      {
#        "chefName"    : self.chefName,
#        "projectName" : aProject,
#        "theProject"  : theProject
#      },
#        0.1
#      )

