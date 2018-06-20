#!/usr/bin/env python
# -*- coding:utf-8 -*-
from run import app
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from exts import db
import config

app.config.from_object(config)
db.init_app(app)


manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()