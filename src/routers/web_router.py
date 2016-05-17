import os
import sys
# import smtplib
from sqlite3 import IntegrityError
from flask import Blueprint
from flask import render_template, request, flash, Response, session
from flask import redirect, make_response, url_for, send_from_directory
from functools import wraps
from datetime import datetime,timedelta

from ..helpers import generate_token

modelsPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../models')
sys.path.append(modelsPath)
from ..models.user_model import UserModel
from ..models.auth_token_model import AuthTokenModel


class WebRouter(Blueprint):
    def register(self, app, options, first_registration=False):
        super(WebRouter, self).register(app, options, first_registration=False)
        self.config = app.config

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
                    if authToken is None or not authToken.isValid():
                        return make_response(redirect(url_for('.login')))

                    user = UserModel.getByPk(authToken.user_id)
                    if user is None:
                        return make_response(redirect(url_for('.login')))
                    if user.isBlocked() or user.isPending():
                        return make_response(redirect(url_for('.login')))
                    if user.role in roles:
                        return api_method(*args, **kwargs)

                    return make_response(redirect(url_for('.query')))

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

            return Response(render_template('login.html'))

        @self.route('/login', methods=['POST'])
        def do_login():
            username = request.form.get('username')
            password = request.form.get('password')
            response = make_response(redirect(url_for('.login')))

            if username is None or password is None:
                flash('Invalid username or password', 'danger')

            user = UserModel.getByUsername(username)
            if user is None:
                flash('Invalid username or password', 'danger')
            else:
                try:
                    token = user.generateToken(password)
                    token.save()
                    response.set_cookie('auth-token', token.token)
                except ValueError as e:
                    flash(e.__str__(), 'danger')

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
            form = session.get('form', {})
            if 'form' in session:
                del session['form']
            return render_template('register.html', form=form)

        @self.route('/register', methods=["POST"])
        def do_register():
            try:
                user = UserModel()
                user.role = 'user'
                user.status = 'not-verified'
                user.requests_made = 0
                user.requests_limit = int(request.form.get("requests_limit"))
                user.username = request.form.get("username")
                user.email = request.form.get("email")
                user.project = request.form.get("project")
                user.note = request.form.get("note")

                if request.form.get("password") != request.form.get("confirm_password"):
                    session['form'] = request.form
                    flash('Passwords do not match', 'danger')
                    return make_response(redirect(url_for('.register')))

                user.setPassword(request.form.get("password"))
                user.activation_token = generate_token()
                user.save()

                note = request.form.get("note", "")
                dc['mail_service'].sendEmailConfirmationEmail(
                    user.username,
                    user.email,
                    url_for('.confirm_email', activation_token=user.activation_token, _external=True))

            except IntegrityError as e:
                session['form'] = request.form
                if e.message == 'UNIQUE constraint failed: users.username':
                    flash('Username ' + request.form.get('username') + ' is already in use', 'danger')
                elif e.message == 'UNIQUE constraint failed: users.email':
                    flash('Email ' + request.form.get('email') + ' is already in use', 'danger')

                return make_response(redirect(url_for('.register')))
            except ValueError as e:
                session['form'] = request.form
                flash('Invalid value for monthly request limit', 'danger')
                return make_response(redirect(url_for('.register')))

            return render_template('register_success.html', login_url=url_for('.login'))

        @self.route('/forgot_password')
        def forgot_password():
            form = session.get('form', {})
            if 'form' in session:
                del session['form']
            return render_template('forgot_password.html', form=form)

        @self.route('/forgot_password', methods=["POST"])
        def forgot_password_send_email():
                email = request.form.get("email")
                user = UserModel.getByEmail(email)
                if user is not None:
                    user.password_reset_token = generate_token()
                    user.password_reset_expiration_token= datetime.now()
                    user.save()

                    dc['mail_service'].sendEmailForgotPasswordEmail(
                        user.username,
                        user.email,
                        url_for('.forgot_password_email', password_reset_token=user.password_reset_token, _external=True))

                    return render_template('forgot_password_email_sent.html')
                else:
                    flash('This e-mail does not exist in our database', 'danger')
                    return make_response(redirect(url_for('.forgot_password')))

        @self.route('/forgot_password_email/<password_reset_token>', methods=["GET"])
        def forgot_password_email(password_reset_token):
            try:
                user = UserModel.getByAttributeSingle('password_reset_token', password_reset_token)
                if user is not None:
                    if (datetime.now() - datetime.strptime(user.password_reset_expiration_token,'%Y-%m-%d %H:%M:%S.%f')) < timedelta(minutes = 15):
                        return render_template('reset_password.html', user_id=user.id, password_reset_token=password_reset_token)
                    else:
                        flash('Your password reset token is expired.', 'danger')
                        return make_response(redirect(url_for('.forgot_password')))
                else:
                    flash('Your token is not valid anymore. Get new one!' , 'danger')
                    return make_response(redirect(url_for('.forgot_password')))
                    
            except ValueError as e:
                flash(e.message, 'danger')
                return make_response(redirect(url_for('.forgot_password')))

        @self.route('/reset_password')
        def reset_password():
            form = session.get('form', {})
            if 'form' in session:
                del session['form']
            return render_template('reset_password.html', form=form)

        @self.route('/reset_password', methods=["POST"])
        def do_reset_password():
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            user_id = request.form.get("user_id")
            password_reset_token = request.form.get("password_reset_token")

            user = UserModel.getByAttributesSingle(['id', 'password_reset_token'], [user_id, password_reset_token])
            if request.form.get("password") != request.form.get("confirm_password"):
                session['form'] = request.form
                flash('Passwords do not match', 'danger')
                return make_response(redirect(url_for('.forgot_password_email', password_reset_token=password_reset_token)))

            user.setPassword(request.form.get("password"))
            user.save()
            return render_template('reset_success.html',login_url=url_for('.login'))

        @self.route('/confirm_email/<activation_token>', methods=["GET"])
        def confirm_email(activation_token):
            try:
                user = UserModel.getByAttributeSingle('activation_token', activation_token)
                user.status = 'pending'
                user.activation_token = None
                user.save()
                dc['mail_service'].sendAccessRequestEmail(user.username, user.note, url_for('.login', _external=True))
                return render_template('activate_success.html', login_url=url_for('.login'))
            except ValueError as e:
                flash('Error activating account', 'danger')
                return make_response(redirect(url_for('.login')))

        @self.route('/query')
        @authenticate(['admin', 'user'])
        def query():
            return render_template('search.html')

        @authenticate(['user'])
        @self.route('/download', methods=['GET'])
        def download():
            auth_token_string = request.cookies.get('auth-token')
            authToken = AuthTokenModel.getByAttributeSingle('token', auth_token_string)

            return send_from_directory(directory=self.config['UPLOAD_FOLDER'], filename=authToken.user_id.__str__())


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
                'admin': 'Admin',
                'user': 'User'
            }
            return render_template('edit-user.html', user=user, statuses=statuses, roles=roles)

        @self.route('/user/<id>/edit', methods=["POST"])
        @authenticate(['admin'])
        def do_edit(id):
            user = UserModel.getById(id)
            old_status = user.status
            user.status = request.form.get("status", "")
            user.requests_limit = request.form.get("requests_limit", "")
            user.save()

            if old_status != 'active' and user.status == 'active':
                dc['mail_service'].sendUserActivatedEmail(user.username, user.email, url_for('.login', _external=True))

            elif old_status != 'blocked' and user.status == 'blocked':
                dc['mail_service'].sendUserBlockedEmail(user.username, user.email)

            return make_response(redirect(url_for('.admin')))

        @self.route('/user/<id>/delete_user', methods=["GET"])
        @authenticate(['admin'])
        def delete_user(id):
            user = UserModel.getById(id)
            user.delete()
            return make_response(redirect(url_for('.admin')))

        @self.route('/admin')
        @authenticate(['admin'])
        def admin():
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
                dc['mail_service'].sendUserBlockedEmail(user.username, user.email)

            return make_response(redirect(url_for('.admin')))

        @self.route('/user/<id>/activate', methods=["POST"])
        @authenticate(['admin'])
        def activate_user(id):
            user = UserModel.getByPk(id)
            oldStatus = user.status
            if user is not None:
                user.activate()
                user.save()
                if oldStatus == 'pending':
                    dc['mail_service'].sendUserActivatedEmail(user.username, user.email, url_for('.login', _external=True))
                else:
                    dc['mail_service'].sendUserReactivatedEmail(user.username, user.email, url_for('.login', _external=True))

            return make_response(redirect(url_for('.admin')))
