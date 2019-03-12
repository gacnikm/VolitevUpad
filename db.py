from peewee import *

db = SqliteDatabase(None)

class Tweet(Model):
    id = TextField()
    user = CharField()
    date = DateField()

    class Meta:
        database = db
