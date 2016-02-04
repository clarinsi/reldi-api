import os
import sys
from flask import Blueprint
from flask import render_template

sys.path.append(os.path.realpath('db'))
from user_db import UserActiveRecord

class WebRouter(Blueprint):
   def __init__(self, dc):
        templateFolder = os.path.realpath('src/web/templates')
        staticFolder = os.path.realpath('src/web/templates/static')
        Blueprint.__init__(self, 'web_router', 'web_router', template_folder=templateFolder, static_folder=staticFolder)

        @self.route('/')
        def index(name):
            user = UserActiveRecord.getByUsernameAndPassword('fpetkovski', '1004989')
            return render_template('admin.html', name = name)


