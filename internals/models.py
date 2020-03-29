from peewee import *
from playhouse.db_url import connect
import os

from internals.context import Context


class BaseModel(Model):
    class Meta:
        database = Context.db

class NotFoundError(Exception):
    def __init__(self):
        self.message = "requested resource not found"
    
class InvalidRequestError(Exception):
    pass

class MissingInputError(InvalidRequestError):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class InvalidInputError(InvalidRequestError):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message