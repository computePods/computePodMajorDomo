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
      'projects'             : {}
    }

    @natsClient.subscribe("build.getExternalDependencies.>")
    async def getExternalDependencies(subject, data) :
      await self.sendExternalDependencies(subject, data)

  def listProjects(self) :
    """List known projects"""

    projects = self.projectData['projects']
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

  # We might want to dynamically add fields to a pydantic object
  # to do this see:
  # https://github.com/samuelcolvin/pydantic/issues/1937#issuecomment-695313040
  #
  def normalizeProject(self, projectDetails) :

    projDesc = projectDetails.projectDesc
    targets = projDesc.targets
    if 'defaults' in targets :
      defaults = targets['defaults']
      for aName, aDef in targets.items() :
        if aName == 'defaults' : continue
        if not aDef.srcDir    : aDef.srcDir    = defaults.srcDir
        if not aDef.outputDir : aDef.outputDir = defaults.outputDir
        if not aDef.mainFile  : aDef.mainFile  = defaults.mainFile
        if not aDef.worker    : aDef.worker    = defaults.worker
        if not aDef.help      : aDef.help      = defaults.help
        if not aDef.install   : aDef.install   = defaults.install
        aDef.uses          = self.mergeArrays(aDef.uses,          defaults.uses)
        aDef.outputs       = self.mergeArrays(aDef.outputs,       defaults.outputs)
        aDef.origExternals = self.mergeArrays(aDef.origExternals, defaults.origExternals)
        aDef.origExternals = self.mergeArrays(aDef.origExternals, defaults.externals)
        aDef.origExternals = self.mergeArrays(aDef.origExternals, aDef.externals)
        aDef.externals     = [ ]
        aDef.dependencies  = self.mergeArrays(
          aDef.dependencies, defaults.dependencies
        )
        aDef.projectDir = projectDetails.projectDir

  async def sendGetExternalDependencies(self, projectDetails) :
    workers = {}
    projTargets = projectDetails.projectDesc.targets
    for aTargetName, aTargetDesc in projTargets.items() :
      if aTargetDesc.worker : workers[aTargetDesc.worker] = True

    for aWorker in workers.keys() :
      await self.nc.sendMessage(
        f"build.getExternalDependencies.{aWorker}",
        None
      )

  async def addedProject(self, projectDetails) :
    """Add the project definition"""

    self.normalizeProject(projectDetails)

    projectName = projectDetails.projectName

    projects = self.projectData['projects']
    if projectName not in projects :
      projects[projectName] = projectDetails
      await self.sendGetExternalDependencies(projectDetails)
      return True
    return False

  async def updatedProject(self, projectDetails) :
    """Update the project definition"""

    self.normalizeProject(projectDetails)

    projectName = projectDetails.projectName
    projects = self.projectData['projects']
    if projectName in projects :
      projects[projectName] = projectDetails
      await self.sendGetExternalDependencies(projectDetails)
      return True
    return False

  async def removedProject(self, projectDetails) :
    """Remove the project definition"""

    projectName = projectDetails.projectName
    projects = self.projectData['projects']
    if projectName in projects :
      del projects[projectName]
      await self.sendGetExternalDependencies(projectDetails)
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
    aDef.externals = [ ]
    for anExternal in aDef.origExternals :
      aDef.externals.append(anExternal)
    for aUse in aDef.uses :
      if aUse.find(':') < 0 : continue
      pkgName, pkgTarget = aUse.split(':')
      if pkgName in projects :
        aProjTargets = projects[pkgName].projectDesc.targets
        if pkgTarget in aProjTargets :
          aTarget = aProjTargets[pkgTarget]
          installDir = aTarget.install['dir']
          if aTarget.outputs :
            for anOutput in aTarget.outputs :
              aDef.externals.append(os.path.join(installDir, anOutput))

  def returnBuild(self, project, target) :
    """Return the build details for the given target of a project."""

    buildDef = {}

    projectsData = self.projectData['projects']
    #return projectsData

    if project in projectsData :
      projectDef = projectsData[project].projectDesc
      if target in projectDef.targets :
        buildDef = projectDef.targets[target]
    #return repr(type(buildDef))

    self.updateExternals(buildDef)
    return buildDef

  async def sendExternalDependencies(self, origSubject, data) :
    origSubject = ".".join(origSubject[3:len(origSubject)])
    projects = self.projectData['projects']
    uses = {}
    for project in projects :
      projectDef = projects[project].projectDesc
      for target in projectDef.targets :
        targetDef = projectDef.targets[target]
        for aUse in targetDef.uses :
          uses[aUse] = True

    extDeps = {}
    for aUse in uses :
      if aUse.find(':') < 0 : continue
      pkgName, pkgTarget = aUse.split(':')
      if pkgName in projects :
        aProjTargets = projects[pkgName].projectDesc.targets
        if pkgTarget in aProjTargets :
          aTarget = aProjTargets[pkgTarget]
          if aTarget.worker != origSubject : continue
          extDeps[aUse] = {
            'project'      : pkgName,
            'target'       : pkgTarget,
            'projectDir'   : aTarget.projectDir,
            'installDir'   : aTarget.install['dir'],
            'manualUpdate' : aTarget.install['manualUpdate'],
            'outputDir'    : aTarget.outputDir,
            'outputs'      : aTarget.outputs,
            'worker'       : aTarget.worker,
            'rsyncUser'    : projects[pkgName].rsyncUser,
            'rsyncHost'    : projects[pkgName].rsyncHost,
          }
    await self.nc.sendMessage(
      f"build.externalDependencies.{origSubject}",
      extDeps
    )

