import os
import sys
from flask import Blueprint
from flask import render_template

modelsPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../models')
sys.path.append(modelsPath)
from user_model import UserModel

class WebRouter(Blueprint):
   def __init__(self, dc):
        templateFolder = os.path.realpath('src/web/templates')
        staticFolder = os.path.realpath('src/web/templates/static')
        Blueprint.__init__(self, 'web_router', 'web_router', template_folder=templateFolder, static_folder=staticFolder)

        @self.route('/login')
        def index():
            user = UserModel.getByUsername('admin')
            return render_template('login.html', name = 'Filip')

       	@self.route('/login')
        def index():
            user = UserModel.getByUsername('admin')
            return render_template('login.html', name = 'Filip')


