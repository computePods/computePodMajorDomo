"""Add the projects interface."""

import yaml

from cpinterfaces.python.projectDetails import ProjectDetails

import logging
logger = logging.getLogger("majorDomo")

def implementProjectInterfaces(self) :

  @self.app.get_projects
  async def get_projects_impl() :
    return self.managers.projects.listProjects()

  @self.app.post_project_add
  async def post_project_add_impl(projectDetails: ProjectDetails) :
    result = "Not added"
    if self.managers.projects.addedProject(projectDetails) :
      result = "Added"
    return {
      'result'      : result,
      'projectName' : projectDetails.projectName,
      'projectDir'  : projectDetails.projectDir
    }

  @self.app.post_project_update
  async def post_project_update_impl(projectDetails: ProjectDetails) :
    result = "Not updated"
    if self.managers.projects.updatedProject(projectDetails) :
      result = "Updated"
    return {
      'result'      : result,
      'projectName' : projectDetails.projectName,
      'projectDir'  : projectDetails.projectDir
    }

  @self.app.post_project_remove
  async def post_project_remove_impl(projectDetails: ProjectDetails) :
    result = "Not removed"
    if self.managers.projects.removedProject(projectDetails) :
      result = "Removed"
    return {
      'result'      : result,
      'projectName' : projectDetails.projectName,
      'projectDir'  : projectDetails.projectDir
    }

  @self.app.get_project_targets
  async def get_project_targets_impl(project) :
    return self.managers.projects.listTargets(project)
