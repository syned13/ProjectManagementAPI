from internals.project import utils
from internals.project import models
from internals.project.models import Project, ProjectEmployee

from internals import models as shared_models

from internals.employee.employee import Employee
from internals.employee import service as employee_service

def add_project(body):
    utils.validate_project_fields(body)
    leader = Employee()

    try:
        leader = employee_service.get_employee(body["leader_id"])
    except shared_models.NotFoundError:
        raise shared_models.InvalidInputError("leader id does not exist")
    
    models.Project.create(project_type=body["type"], name=body["name"], budget=body["budget"], leader=leader)
    

def get_all_projects():
    raw_projects = models.Project.select().execute()
    projects = []
    for project in  raw_projects:
        raw_project_employee = ProjectEmployee.select().where(ProjectEmployee.project == project)
        for project_employee in raw_project_employee:
            project.employees.append(project_employee.employee.id)

        projects.append(project.to_json())
    
    return projects

def update_project(body):
    utils.validate_project_fields(body)
    if body.get("id") == None:
        raise shared_models.MissingInputError("missing project id")

    leader = Employee()
    
    try:
        leader = employee_service.get_employee(body["leader_id"])
    except shared_models.NotFoundError:
        raise shared_models.InvalidInputError("leader id does not exist")
    
    project = Project(project_type=body["type"], name=body["name"], budget=body["budget"], leader=leader)
    project.save()

def get_project(id):
    try:
        return models.Project.get(models.Project.id == id)
    except models.Project.DoesNotExist:
        raise shared_models.NotFoundError

def remove_project(id):
    try:
        if Project.delete().where(Project.id == id).execute() == 0:
            raise shared_models.NotFoundError()
    except Employee.DoesNotExist:
        raise shared_models.NotFoundError()

def add_employee_to_project(project_id, employee_id):
    try:
        project = models.Project.get(models.Project.id == project_id)
        employee = employee_service.get_employee(employee_id)
        ProjectEmployee.create(project=project, employee=employee)
    except models.Project.DoesNotExist:
        raise shared_models.NotFoundError

def remove_employee_from_project(project_id, employee_id):
    try:
        project = get_project(project_id)
        employee = employee_service.get_employee(employee_id)

        if ProjectEmployee.delete().where(ProjectEmployee.project == project and ProjectEmployee.employee == employee) == 0:
            raise shared_models.NotFoundError
    
    except ProjectEmployee.DoesNotExist:
        raise shared_models.NotFoundError()
