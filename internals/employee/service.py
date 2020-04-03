from peewee import *

from internals.context import Context
from internals import models
from internals.employee.employee import Employee
from internals.employee.address import Address
from internals.employee.phone import Phone, PhoneType

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
        return Employee.get(Employee.id == id)
    except Employee.DoesNotExist:
        raise models.NotFoundError

def remove_employee(id):
    try:
        if Employee.delete().where(Employee.id == id).execute() == 0:
            raise models.NotFoundError
    except Employee.DoesNotExist:
        Context.db.rollback()
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

def add_phone(body):
    validate_phone_fields(body)
    try:
        employee = get_employee(body["owner_id"])
    except models.NotFoundError:
        raise models.InvalidInputError("owner id does not exist")
    try:
        Phone.create(phone_type=body["phone_type"], phone_number=body["phone_number"], area_code=body["area_code"], owner=employee)
    except IntegrityError as e:
        Context.db.rollback()
        raise models.InvalidInputError("duplicate phone number")

def remove_phone(phone_number, area_code):
    try:
        if Phone.delete().where(Phone.phone_number == phone_number and Phone.area_code == area_code).execute() == 0:
            raise models.NotFoundError
    except Employee.DoesNotExist:
        Context.db.rollback()
        raise models.NotFoundError

def get_phone(phone_number, area_code):
    try:
        return Phone.get(Phone.area_code == area_code and Phone.phone_number == phone_number)
    except Phone.DoesNotExist:
        raise models.NotFoundError

def get_all_phones():
    raw_phones = Phone.select().execute()
    phones = []
    for phone in  raw_phones:
        phones.append(phone.to_json())
    
    return phones

def update_phone(body):
    validate_phone_fields(body)
    employee = Employee()
    
    try:
        employee = get_employee(body["owner_id"])
    except models.NotFoundError:
        raise models.InvalidInputError("owner id does not exist")

    phone = Phone(phone_type=body["phone_type"], phone_number=body["phone_number"], area_code=body["area_code"], owner=employee)
    phone.save()


def validate_phone_fields(body):
    if body.get("phone_type") == None:
        raise models.MissingInputError("missing phone type")

    if body.get("phone_number") == None:
        raise models.MissingInputError("missing phone number")
    
    if body.get("area_code") == None:
        raise models.MissingInputError("missing area code")

    if body.get("owner_id") == None:
        raise models.MissingInputError("missing owner id")
    
    if body.get("phone_type") != PhoneType.CELL_PHONE.value and body.get("phone_type") != PhoneType.LOCAL_PHONE.value:
        raise models.InvalidInputError("invalid phone type")


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

        
