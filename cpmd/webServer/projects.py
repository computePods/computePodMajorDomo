"""Add the projects interface."""

import yaml

def implementProjectInterfaces(self) :

  @self.app.get_projects
  async def get_projects_impl() :
    projects = self.managers.projects.projectData['projects']
    projectsDict = {}
    for aProject, projectDetails in projects.items() :
      projectsDict[aProject] = projectDetails['path']
    return projectsDict
