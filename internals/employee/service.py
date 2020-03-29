from peewee import *

from internals import models
from internals.employee.employee import Employee
from internals.employee.address import Address

def add_new_employee(body):
    validate_employee_fields(body)
    validate_address(body["address"])

    address = Address(street=body["address"]["street"], city=body["address"]["city"], province=body["address"]["province"], country=body["address"]["country"], postcode=body["address"]["postcode"])
    address.save()

    employee = Employee(first_name=body["first_name"], last_name=body["last_name"], salary=body["salary"], start_date=body["start_date"], address_id=address.id)
    employee.save()

def get_all_employees():
    raw_employees = Employee.select().execute()
    employees = []
    for employee in  raw_employees:
        employees.append(employee.to_json())
    
    return employees

def get_employee(id):
    try:
        return Employee.get(Employee.id == id).to_json()
    except Employee.DoesNotExist:
        raise models.NotFoundError

def remove_employee(id):
    try:
        if Employee.delete().where(Employee.id == id).execute() == 0:
            raise models.NotFoundError
    except Employee.DoesNotExist:
        raise models.NotFoundError

def update_employee(body):
    if body.get("id") == None:
        raise models.MissingInputError("missing employee id")

    validate_employee_fields(body)
    validate_address(body["address"])

    if body["address"].get("id") == None:
        raise models.MissingInputError("missing address id")

    address = Address(id=body["address"]["id"], street=body["address"]["street"], city=body["address"]["city"], province=body["address"]["province"], country=body["address"]["country"], postcode=body["address"]["postcode"])
    address.save()

    employee = Employee(id=body["id"], first_name=body["first_name"], last_name=body["last_name"], salary=body["salary"], start_date=body["start_date"], address_id=address.id)
    employee.save()

def validate_employee_fields(body):
    if body.get("first_name") == None:
        raise models.MissingInputError("missing first name")

    if body.get("last_name") == None:
        raise models.MissingInputError("missing last name")

    if body.get("salary") == None:
        raise models.MissingInputError("missing salary")
    
    if body.get("start_date") == None:
        raise models.MissingInputError("missing start date")
    
    if body.get("address") == None:
        raise models.MissingInputError("missing address")


def validate_address(address):
    if address.get("street") == None:
        raise models.MissingInputError("missing address street")

    if address.get("city") == None:
        raise models.MissingInputError("missing address city")

    if address.get("province") == None:
        raise models.MissingInputError("missing address street")
    
    if address.get("country") == None:
        raise models.MissingInputError("missing address country")
    
    if address.get("postcode") == None:
        raise models.MissingInputError("missing address postcode")

        
