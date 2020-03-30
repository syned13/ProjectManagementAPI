from flask import Flask, Blueprint, request, jsonify

from internals.project import service
from internals import models as shared_models

project_controller = Blueprint("project_controller", __name__)

@project_controller.route("/project", methods=["GET","POST","PUT"])
def project():
    if request.method == "GET":
        return jsonify(service.get_all_projects())
    
    body = {}
    try:
        body = request.get_json(force=True)
    except:
        return jsonify({"message":"no json provided as body"}), 400

    try:
        if request.method == "POST":
            service.add_project(body)
            return jsonify({"message":"project created"})
        
        if request.method == "PUT":
            service.update_project(body)
            return jsonify({"message":"project updated"})

    except shared_models.InvalidRequestError as e:
            return jsonify({"message": str(e)}), 400


   
@project_controller.route("/project/<int:id>", methods=["GET", "DELETE"])
def specific_project(id):
    try:
        if request.method == "GET":
            return jsonify(service.get_project(id).to_json())
        if request.method == "DELETE":
            service.remove_project(id)
            return jsonify({"message":"project deleted"})
    except shared_models.NotFoundError as e:
        return jsonify({"message": str(e.message)}), 404

    return ""

@project_controller.route("/project/<int:project_id>/employee/<int:employee_id>", methods=["POST", "DELETE"])
def project_employee(project_id, employee_id):
    try:
        if request.method == "POST":
            service.add_employee_to_project(project_id, employee_id)
            return jsonify({"message":"employee added to project"})
        if request.method == "DELETE":
            service.remove_employee_from_project(project_id, employee_id)
            return jsonify({"message":"employee removed from project"})
    
    except shared_models.InvalidRequestError as e:
        return jsonify({"message": str(e.message)}), 400
    except shared_models.NotFoundError as e:
        return jsonify({"message": str(e.message)}), 404

