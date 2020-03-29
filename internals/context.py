from peewee import *
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
from playhouse.db_url import connect

import os
from urllib import parse


class Context():
    db = connect(os.getenv("DB_CONNECTION"))