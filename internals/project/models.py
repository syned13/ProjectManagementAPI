from peewee import *
from enum import Enum

from internals import models
from internals import context

from internals.employee import address
from internals.employee import employee

class Project(models.BaseModel):
    project_type = TextField()
    name = TextField()
    budget = DoubleField()
    leader = ForeignKeyField(employee.Employee, backref="leader")

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.employees = []
        

    def to_json(self):
        return {
            "project_type":self.project_type, 
            "id": self.id,
            "name":self.name, 
            "budget":self.budget, 
            "leader":self.leader.to_json(), 
            "employees_ids": self.employees
        }

class ProjectEmployee(models.BaseModel):
    project = ForeignKeyField(Project, backref="project")
    employee = ForeignKeyField(employee.Employee, backref="employee")

    def to_json(self):
        return {
            "employee": self.employee.to_json(),
            "project": self.project.to_json(),
        }
    class Meta():
        primary_key = CompositeKey('project','employee')
class ProjectType(Enum):
    FINANCE_PROJECT = "finance_project"
    ENGINEERING_PROJECT = "engineering_project"
    DESIGN_PROJECT = "design_project"
