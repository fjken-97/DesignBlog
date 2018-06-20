#!/usr/bin/env python
# -*- coding:utf-8 -*-

DIALECT='mysql'
DRIVER='pymysql'
HOSTNAME = '127.0.0.1'
DATABASE='blog'
USERNAME='root'
PASSWORD='fjken1997'
PORT='3306'
DB_URI='{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SECRET_KEY = "MyBlog"

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '25'
MAIL_USE_TLS = 'True'
MAIL_USERNAME = 'myblogserver@163.com'
MAIL_PASSWORD = 'fjken031602219'
