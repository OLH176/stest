import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

from exts import db
class User(db.Model):
    __tablename__="users"
    __table_args__={"useexisting":True}
    username=db.Column(db.String(15),primary_key=True)
    password=db.Column(db.String(15))
    name=db.Column(db.String(15))
    idnum=db.Column(db.String(18))

class Message(db.Model):
    __tablename__="message"
    __table_args__={"useexisting":True}
    id=db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False)
    username=db.Column(db.String(15))
    message=db.Column(db.String(200))

class Ad(db.Model):
    __tablename__="admin"
    __table_args__={"useexisting":True}
    username=db.Column(db.String(15),primary_key=True)
    password=db.Column(db.String(15),nullable=False)

class Userlog(db.Model):
    __tablename__ = "userlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(15), primary_key=True)
    in_time = db.Column(DateTime,default=datetime.datetime.now())
    ip =db.Column(db.String(16))

class Adminlog(db.Model):
    __tablename__ = "adminlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(15), primary_key=True)
    in_time = db.Column(DateTime, default=datetime.datetime.now())
    ip = db.Column(db.String(16))

class Adminoplog(db.Model):
    __tablename__ = "adminoplog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(15), primary_key=True)
    in_time = db.Column(DateTime, default=datetime.datetime.now())
    ip = db.Column(db.String(16))
    op= db.Column(db.String(30))

class Useroplog(db.Model):
    __tablename__ = "useroplog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(15), primary_key=True)
    in_time = db.Column(DateTime, default=datetime.datetime.now())
    ip = db.Column(db.String(16))
    op = db.Column(db.String(30))