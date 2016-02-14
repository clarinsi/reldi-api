import os
import sys
from flask import Blueprint
from flask import render_template, request, flash, Response
from flask import redirect, make_response, url_for
from functools import wraps
from validate_email import validate_email

modelsPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../models')
sys.path.append(modelsPath)
from user_model import UserModel
from auth_token_model import AuthTokenModel

class WebRouter(Blueprint):
   def __init__(self, dc):
        templateFolder = os.path.realpath('src/web/templates')
        staticFolder = os.path.realpath('src/web/templates/static')
        Blueprint.__init__(self, 'web_router', 'web_router', template_folder=templateFolder, static_folder=staticFolder)


        def authenticate(roles):
            def wrapper(api_method):
                @wraps(api_method)
                def check_token(*args, **kwargs):
                    auth_token_string = request.cookies.get('auth-token')
                    authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)
                    if authToken is not None and authToken.isValid():
                        user = UserModel.getByPk(authToken.user_id)
                        if user is not None and user.role in roles:
                            return api_method(*args, **kwargs)
                        elif user is not None:
                            return make_response(redirect(url_for('.query')))
                        else:
                            return make_response(redirect(url_for('.login')))
                    else:
                        return make_response(redirect(url_for('.login')))
                return check_token
            return wrapper

        @self.route('/', methods=['GET'])
        @self.route('/login', methods=['GET'])
        def login():
            auth_token_string = request.cookies.get('auth-token')
            authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)
            if authToken and authToken.isValid():
                user = UserModel.getByPk(authToken.user_id)
                if user.isAdmin():
                    return make_response(redirect(url_for('.admin')))
                else:
                    return make_response(redirect(url_for('.query')))

            response = Response(render_template('login.html'))
            return response

        @self.route('/login', methods=['POST'])
        def do_login():
            username = request.form.get('username')
            password = request.form.get('password')
            response = make_response(redirect(url_for('.login')))

            if username is not None and password is not None:
                user = UserModel.getByUsername(username)
                if user is not None:
                    try:
                        token = user.generateToken(password)
                        token.save()
                        response.set_cookie('auth-token', token.token)
                    except ValueError:
                        flash('Invalid username or password', 'danger')
                    # flash('You were successfully logged in', 'success')
                else:
                    flash('Invalid username or password', 'danger')
            else:
                flash('Invalid username or password', 'danger')

            return response

        @self.route('/logout', methods=["POST"])
        def logout():
            auth_token_string = request.cookies.get('auth-token')
            authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)
            if authToken:
                authToken.delete()

            response = make_response(redirect(url_for('.login')))
            response.set_cookie('auth-token', '', expires=0)

            return response

       	@self.route('/register')
        def register():
            user = UserModel.getByUsername('admin')
            return render_template('register.html', name = 'Filip')

        @self.route('/query')
        @authenticate(['admin', 'user'])
        def query():
            user = UserModel.getByUsername('admin')
            return render_template('search.html', name = 'Filip')

        @self.route('/user/<id>/edit', methods=["GET"])
        @authenticate(['admin'])
        def edit(id):
            user = UserModel.getById(id)
            statuses = {
                'active': 'Active',
                'pending': 'Pending',
                'blocked': 'Blocked'
            }
            roles = {
                'admin' : 'Admin',
                'user' : 'User'
            }
            return render_template('edit-user.html', user=user, statuses=statuses, roles=roles)

        @self.route('/user/<id>/edit', methods=["POST"])
        @authenticate(['admin'])
        def do_edit(id):
            user = UserModel.getById(id)
            user.role = request.form.get("role","")
            user. status= request.form.get("status","")
            user.requests_limit= request.form.get("requests_limit","")
            print user
            user.save()
            return render_template('admin.html')

        @self.route('/register', methods=["POST"])
        def register_user():
            user = UserModel()
            user.role = 'user'
            user. status = 'pending'
            user.requests_made= 0
            user.requests_limit= request.form.get("requests_limit","")
            user.username= request.form.get("username","")
            is_valid = validate_email(request.form.get("email",""))
            if is_valid == 1:
                user.email= request.form.get("email","")
            else:
                raise ValueError("Invalid e-mail address")
            user.project= request.form.get("project","")
            if request.form.get("password","") == request.form.get("confirm_password",""):
                user.setPassword(request.form.get("password",""))
            else:
                raise ValueError("Passwords aren't equal")
            user.save()
            return render_template('admin.html')

        @self.route('/admin')
        @authenticate(['admin'])
        def admin():
            user = UserModel.getByUsername('admin')

            users = UserModel.getByAttribute('role', 'user')
            active_users = filter(lambda x: x.status == 'active', users)
            pending_users = filter(lambda x: x.status == 'pending', users)
            blocked_users = filter(lambda x: x.status == 'blocked', users)

            return render_template(
                'admin.html',
                active_users=active_users,
                pending_users=pending_users,
                blocked_users=blocked_users
            )

        @self.route('/user/<id>/block', methods=["POST"])
        @authenticate(['admin'])
        def block_user(id):
            user = UserModel.getByPk(id)
            if user is not None:
                user.block()
                user.save()

            return make_response(redirect(url_for('.admin')))

        @self.route('/user/<id>/activate', methods=["POST"])
        @authenticate(['admin'])
        def activate_user(id):
            user = UserModel.getByPk(id)
            if user is not None:
                user.activate()
                user.save()

            return make_response(redirect(url_for('.admin')))
