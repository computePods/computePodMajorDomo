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

  def mergeArrays(self, a1, a2) :
    mDict = { }
    if a1 :
      for anItem in a1 : mDict[anItem] = True
    if a2 :
      for anItem in a2 : mDict[anItem] = True
    return list(mDict.keys())

  def normalizeProject(self, projectDetails) :
    projDesc = projectDetails.projectDesc
    targets = projDesc.targets
    if 'defaults' in targets :
      defaults = targets['defaults']
      for aName, aDef in targets.items() :
        if aName == 'defaults' : continue
        if not aDef.outputDir : aDef.outputDir = defaults.outputDir
        if not aDef.worker    : aDef.worker    = defaults.worker
        if not aDef.help      : aDef.help      = defaults.help
        aDef.uses         = self.mergeArrays(aDef.uses,      defaults.uses)
        aDef.outputs      = self.mergeArrays(aDef.outputs,   defaults.outputs)
        aDef.externals    = self.mergeArrays(aDef.externals, defaults.externals)
        aDef.dependencies = self.mergeArrays(
          aDef.dependencies, defaults.dependencies
        )
        aDef.projectDir = projectDetails.projectDir

  def addedProject(self, projectDetails) :
    """Add the project definition"""

    self.normalizeProject(projectDetails)

    projectName = projectDetails.projectName

    projects = self.projectData['projects']
    if projectName not in projects :
      projects[projectName] = projectDetails
      return True
    return False

  def updatedProject(self, projectDetails) :
    """Update the project definition"""

    self.normalizeProject(projectDetails)

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

  def listTargets(self, project) :
    """List known targets for a given project"""

    targets = {}

    projectsData = self.projectData['projects']

    if project in projectsData :
      projectDef = projectsData[project].projectDesc
      for aTargetName, aTargetDef in projectDef.targets.items() :
        if aTargetName == 'defaults' : continue
        targets[aTargetName] = aTargetDef.help

    return targets

  def returnDefinition(self, project) :
    """Return the defintion of a given project"""

    projectDef = {}

    projectsData = self.projectData['projects']

    if project in projectsData :
      projectDef = projectsData[project].projectDesc

    return projectDef

  def updateExternals(self, aDef) :
    projects = self.projectData['projects']
    for aUse in aDef.uses :
      pkgName, pkgTarget = aUse.split(':')
      if pkgName in projects :
        aProjTargets = projects[pkgName].projectDesc.targets
        if pkgTarget in aProjTargets :
          aTarget = aProjTargets[pkgTarget]
          prefix = os.path.join(
            aTarget.projectDir,
            aTarget.outputDir
          )
          if aTarget.outputs :
            for anOutput in aTarget.outputs :
              aDef.externals.append(os.path.join(prefix, anOutput))

  def returnBuild(self, project, target) :
    """Return the build details for the given target of a project."""

    buildDef = {}

    projectsData = self.projectData['projects']
    #return projectsData

    if project in projectsData :
      projectDef = projectsData[project].projectDesc
      if target in projectDef.targets :
        buildDef = projectDef.targets[target]

    self.updateExternals(buildDef)
    return buildDef











