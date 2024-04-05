from datetime import datetime
from extentions import db
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(150))
    password = db.Column(db.String)
    admin = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, default=datetime.now())

class course(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer, default=0)
    content = Column(Text)
    image = Column(String, default='/uploads/default.jpg')
    date_created = Column(DateTime, default=datetime.now())
    updated_corse = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class episode(db.Model):
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    title = Column(String)
    content = Column(Text)
    number = Column(Integer)
    date_created = Column(DateTime, default=datetime.now())
    updated_corse = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def get_course(self):
        return course.query.filter_by(id = self.course_id).one()

class register(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    date_register = Column(DateTime, default=datetime.now())

    def get_course(self):
        return course.query.filter_by(id = self.course_id).one()