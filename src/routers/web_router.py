import os
import sys
from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response

modelsPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../models')
sys.path.append(modelsPath)
from user_model import UserModel

class WebRouter(Blueprint):
   def __init__(self, dc):
        templateFolder = os.path.realpath('src/web/templates')
        staticFolder = os.path.realpath('src/web/templates/static')
        Blueprint.__init__(self, 'web_router', 'web_router', template_folder=templateFolder, static_folder=staticFolder)

        @self.route('/login', methods=['GET'])
        def login():
            return render_template('login.html')

        @self.route('/login', methods=['POST'])
        def do_login():
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username is not None and password is not None:
                user = UserModel.getByUsername(username)
                token = user.generateToken(password)
                

            resp = Response("Hello")
            return resp
            # resp.headers['Access-Control-Allow-Origin'] = '*'
            # return resp
            # user = UserModel.getByUsername('admin')


            # return render_template('login.html', name = 'Filip')

       	@self.route('/register')
        def register():
            user = UserModel.getByUsername('admin')
            return render_template('register.html', name = 'Filip')

        @self.route('/')
        def index():
            user = UserModel.getByUsername('admin')
            return render_template('index.html', name = 'Filip')

        @self.route('/admin')
        def admin():
            user = UserModel.getByUsername('admin')
            return render_template('admin.html', name = 'Filip')

