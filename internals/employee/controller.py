from flask import Blueprint, request, jsonify
import jsonpickle

from internals.employee import service
from internals import models

employee_controller = Blueprint("employee_controller", __name__)


@employee_controller.route("/employee", methods=["GET","POST"])
def employee():
    if request.method == "POST":
        body = {}
        try:
            body = request.get_json(force=True)
        except:
            return jsonify({"message":"no json provided as body"}), 400
        
        try:
            service.add_new_employee(body)
        except models.InvalidRequestError as e:
            return jsonify({"message":str(e)}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "internal server error"}), 500
    
    if request.method == "GET":
        return jsonify(service.get_all_employees())

    return jsonify({"message":"employee created succesfully"}), 201

@employee_controller.route("/employee/<int:id>", methods=["GET", "DELETE", "PUT"])
def get_employee(id):
    if request.method == "GET":
        try:
            return service.get_employee(id)
        except models.NotFoundError  as e:
            return jsonify({"message": str(e.message)}),404
    
    if request.method == "DELETE":
        try:
            service.remove_employee(id)
            return jsonify({"message": "employee deleted"}),200
        except models.NotFoundError  as e:
            return jsonify({"message": str(e.message)}),404
    
    if request.method == "PUT":
        body = {}
        try:
            body = request.get_json(force=True)
        except:
            return jsonify({"message":"no json provided as body"}), 400

        try:
            service.update_employee(body)
            return jsonify({"message":"employee updated succesfully"}), 200
        except models.InvalidRequestError as e:
            return jsonify({"message":str(e)}), 400
    