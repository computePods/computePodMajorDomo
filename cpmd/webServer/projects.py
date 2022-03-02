"""Add the projects interface."""

import yaml

from cpinterfaces.python.projectPath import ProjectPath

def implementProjectInterfaces(self) :

  @self.app.get_projects
  async def get_projects_impl() :
    projects = self.managers.projects.projectData['projects']
    projectsDict = {}
    for aProject, projectDetails in projects.items() :
      projectsDict[aProject] = projectDetails['path']
    return projectsDict

  @self.app.post_project_add
  async def post_project_add_impl(projectPath: ProjectPath) :
    projects = self.managers.projects.projectData['projects']
    if projectPath.projectName not in projects :
      projects[projectPath.projectName] = projectPath.projectDir

  @self.app.post_project_remove
  async def post_project_remove_impl(projectPath: ProjectPath) :
    projects = self.managers.projects.projectData['projects']
    if projectPath.projectName in projects :
      del projects[projectPath.projectName]
