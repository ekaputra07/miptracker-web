from google.appengine.ext import db


class Log(db.Model):
    ip = db.StringProperty(required=True)
    ua = db.TextProperty()
    time = db.DateTimeProperty(auto_now_add=True)
    page = db.StringProperty()