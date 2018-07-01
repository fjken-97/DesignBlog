#!/usr/bin/env python
# -*- coding:utf-8 -*-
from exts import db
from datetime import datetime
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash,check_password_hash

class BlogPost(db.Model):
    __tablename__ = 'blogposted'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime,default=datetime.now)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref = 'blogposted')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    status = db.Column(db.Boolean,default= True)
    login_time = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    # def __str__(self):
    #     return "Users(id='%s')" % self.id

#     @staticmethod
#     def insert_admin(email, username, password):
#         user = User(email=email, username=username, password=password)
#         db.session.add(user)
#         db.session.commit()
#
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
#
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
#
#     def add(self, user):
#         db.session.add(user)
#         return session_commit()
#
#     def get(self, id):
#         return self.query.filter_by(id=id).first()
#
#     def update(self):
#         return session_commit()
#
# def session_commit():
#     try:
#         db.session.commit()
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         reason = str(e)
#         return reason

class Comment(db.Model):
    __tablename__ = 'comm'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogposted.id'))
    audience_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    blog = db.relationship('BlogPost', backref=db.backref('comm', order_by=create_time.desc()))
    audience = db.relationship('User', backref='comm')

# class Vote(db.Model):
#     __tablename__ = 'vote'
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     voter_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
#     blog_id = db.Column(db.Integer, db.ForeignKey('blogposted.id'))
#     up = db.Column(db.Integer,default=0)
#     down = db.Column(db.Integer,default=0)
#
#     blog = db.relationship('BlogPost', backref='vote')
#     voter = db.relationship('User', backref='vote')
