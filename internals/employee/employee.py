from peewee import *

from internals import models
from internals import context

from internals.employee import address

class Employee(models.BaseModel):
    first_name = TextField()
    last_name = TextField()
    salary = DoubleField()
    start_date = DateField()
    end_date = DateField(null=True)
    manager_d = BigIntegerField(null=True)
    address = ForeignKeyField(address.Address, backref="address")

    def to_json(self):
        return {
            "first_name":self.first_name, 
            "last_name":self.last_name, 
            "salary":self.salary, 
            "start_date":self.start_date, 
            "end_date":self.end_date,
            "address": self.address.to_json(),
            "id":self.id,
        }

