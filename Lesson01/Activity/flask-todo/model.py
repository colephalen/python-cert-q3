from peewee import Model, CharField, DateTimeField, ForeignKeyField
import os

from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class User(Model):
    # TODO: Add model fields here
    username = CharField(max_length=255, unique=True)  # why 255?
    password = CharField(max_length=255)

    class Meta:
        database = db


class Task(Model):
    name = CharField(max_length=255)
    performed = DateTimeField(null=True) # datetime or None if there is no task posted
    performed_by = ForeignKeyField(model=User, null=True)  # or None if no task posted

    class Meta:
        database = db

