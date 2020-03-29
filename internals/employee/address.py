from peewee import *

from internals import models

class Address(models.BaseModel):
    street = TextField()
    city = TextField()
    province = TextField()
    country = TextField()
    postcode = TextField()

    def to_json(self):
        return {
            "street": self.street,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "postcode": self.postcode,
            "id":self.id,
        }