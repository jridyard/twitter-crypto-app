
# # Flask
# from flask import render_template, redirect, url_for, make_response, jsonify, request
# from flask_login import login_user, logout_user, login_required, current_user

# # 'app' Folder
# from app import db, login_manager
# from app.base import blueprint
# from app.base.models import User
# from app.base.util import verify_pass

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, make_response
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User, AccessCodes

from app.base.util import verify_pass

@blueprint.route('/base/blueprint')
def route_default():
    return redirect(url_for('home.influencers'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.influencers'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        email = request.form['email'].lower()
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(email=email).first()

        # # # users = User.query.all()
        # # # for x in users:
        # # #     print(x.__dict__)
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('home.influencers'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)

    return redirect(url_for('home.influencers'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
            username  = request.form['username'].lower()
            form_email     = request.form['email'   ].lower()
            access_code = request.form['access_code']
            print("Access code is " + access_code)
            
            print(form_email)
            # Check usename exists
            user = User.query.filter_by(username=username).first()
            if user:
                return render_template( 'accounts/register.html',
                                        msg='Username already registered',
                                        success=False,
                                        form=create_account_form)

            # Check email exists
            email = User.query.filter_by(email=form_email).first()
            print(email)
            if email or form_email == None:
                return render_template( 'accounts/register.html', 
                                        msg='Email already registered', 
                                        success=False,
                                        form=create_account_form)

            # Check access code is valid
            access_code_from_db = AccessCodes.query.filter(AccessCodes.access_code == access_code).first()

            print("This down here...")
            # else we can create the user
            credsToGive = 1000
            subscription = "Free"
            role = "Regular"
            licenses=5

            if access_code == 'FEEM-XG7C-3WG9-GG69' or access_code == 'MXEQ-MFGD-6Z89-NSM3':
                if access_code_from_db == None:
                    credsToGive = 10000000
                    subscription = "Admin"
                    role = "Admin"
                    licenses = 1000
                    
                    new_access_code = AccessCodes(access_code=access_code, access_permissions="Admin", username=username, email=email)
                    db.session.add(new_access_code)
                    db.session.commit()
                else:
                    return render_template( 'accounts/register.html', 
                        msg='Access Code Already Used.', 
                        success=False,
                        form=create_account_form)
            elif access_code_from_db == None:
                    return render_template( 'accounts/register.html', 
                        msg='Access Code Invalid.', 
                        success=False,
                        form=create_account_form)
            elif access_code_from_db.email != "":
                print('sdsdsd')
                return render_template( 'accounts/register.html', 
                    msg='Access Code Already Used.', 
                    success=False,
                    form=create_account_form) 

            # Access code is valid, assign properties so its bound to that user only
            if access_code_from_db:
                access_code_from_db.username = username
                access_code_from_db.email = form_email
                
            user = User(
                    username=username,
                    email=form_email,
                    password=request.form['password'],
                    credits=credsToGive,
                    theme_preference="Light",
                    subscription=subscription,
                    subscription_credits=credsToGive,
                    role=role,
                    access_code=access_code,
                    licenses=licenses
                )
            db.session.add(user)
            db.session.commit()

            print(user)

            password = request.form['password']


            # Locate user
            user = User.query.filter_by(email=form_email).first()

            print('hjave it here')
            print(user)

            
            # Check the password
            if user and verify_pass( password, user.password):

                login_user(user)
                return redirect(url_for('home.influencers') + "#new-user")

    else:
        return render_template( 'accounts/register.html', form=create_account_form) #accounts/register.html'