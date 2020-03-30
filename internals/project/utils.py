from internals import models
from internals.project.models import ProjectType

def validate_project_fields(body):
    if body.get("type") == None:
        raise models.MissingInputError("missing project type")

    if body["type"] != ProjectType.DESIGN_PROJECT.value and body["type"] != ProjectType.ENGINEERING_PROJECT.value and body["type"] != ProjectType.FINANCE_PROJECT.value:
        raise models.InvalidInputError("invalid project type")

    if body.get("name") == None:
        raise models.MissingInputError("missing project name")

    if body.get("budget") == None:
        raise models.MissingInputError("missing project budget")

    if body.get("leader_id") == None:
        raise models.MissingInputError("missing project leader")

    