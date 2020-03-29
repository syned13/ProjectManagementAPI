from flask import Flask
from dotenv import load_dotenv
from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
import os
from playhouse.db_url import connect

#loads env variables from the .env file
load_dotenv()

from config import config
from internals.context import Context
from internals.employee import controller as employee_controller

from internals.employee import employee
from internals.employee import phone
from internals.employee import address

#sets the flask app
app = Flask(__name__)
app.config.from_object(config["development"])


Context.db.create_tables([employee.Employee, address.Address, phone.Phone])

#routes
app.register_blueprint(employee_controller.employee_controller)


@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.run()