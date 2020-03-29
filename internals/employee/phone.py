from peewee import *
from enum import Enum

from internals import models
from internals import context

from internals.employee import employee

class Phone(models.BaseModel):
    phone_type = TextField()
    phone_number = TextField()
    area_code = TextField()
    owner = ForeignKeyField(employee.Employee, backref="owner")

    def to_json(self):
        return {
            "phone_type": self.phone_type,
            "phone_number": self.phone_number,
            "area_code": self.area_code,
            "owner_id": self.owner.id,
        }

    class Meta:
        primary_key = CompositeKey('phone_number','area_code')

class PhoneType(Enum):
    CELL_PHONE = "cell_phone"
    LOCAL_PHONE = "local_phone"