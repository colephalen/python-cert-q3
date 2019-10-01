"""
Scripts to run to set up our database. copied from module 
"""
from passlib.hash import pbkdf2_sha256

from datetime import datetime
from model import db, User, Task


# Create the database tables for our model
db.connect()
db.drop_tables([User, Task])
db.create_tables([User, Task])

Task(name="Do the laundry.").save()
Task(name="Do the dishes.", performed=datetime.now()).save()

User(username="admin", password=pbkdf2_sha256.hash("password")).save()
User(username="bob", password=pbkdf2_sha256.hash("bobbob")).save()
