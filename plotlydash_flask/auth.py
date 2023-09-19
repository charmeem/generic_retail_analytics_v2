import flask
from flask import Blueprint, redirect, render_template, flash, request, session, url_for, jsonify, make_response
from flask_login import login_required, logout_user, current_user, login_user
from forms import LoginForm, SignupForm
from models import db, User
from datetime import datetime as dt
# from . import login_manager
from extensions import login_manager
# from . import login_manager
from sqlalchemy.exc import IntegrityError


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# @auth_bp.route('/app_1')
# # @main_bp.route('/app_1_raw_dash')
# @login_required
# def app_1_template():
#     # return render_template('dash.html', dash_url='/app_1_raw_dash/')
#     return flask.redirect('/app_1_raw_dash')

# @auth_bp.errorhandler(IntegrityError)
# def handle_integrity_error(e):
#     # Customize the error message as needed
#     error_message = "Username already exists. Please choose a different one."
    
#     # You can also log the error for debugging purposes
#     # app.logger.error(str(e))

#     # Return a JSON response with the error message and a 400 status code
#     return jsonify({'error': error_message}), 400

""" Creating Users via SIGNUP FORM """
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    
        
    form = SignupForm()
    if form.validate_on_submit():
        print("hiiiiiiiiiiiiiii")
        #check if user email or user is already created
        existing_user = User.query.filter(User.username==form.username.data).first()
        existing_email = User.query.filter(User.email==form.email.data ).first()
        
        #inserting data into database via ORM User model models.py
        if existing_user:
            return make_response(
                    f'{form.username.data} already created!'
                )
            flash('A user already exists ')
        elif existing_email:
            return make_response(
                    f'{form.email.data} already created!'
                )
            flash('email already exists .')    
            
        user = User(
            username=form.username.data,
            email=form.email.data,
            appid=form.appid.data,
            created_on = dt.now(),
            admin=False,
        )
        user.set_password(form.password.data)
        db.session.add(user) #Staging the new user to be added to database
        db.session.commit()  # Create new user and adds it to the database
        login_user(user)  # Log in as newly created user
        return redirect('/login')
    
    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )
        
    
    

# An alternate way of showing the error in nice way instead of error interrupting the execution

# """ Creating Users via SIGNUP FORM """
# @auth_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     """
#     User sign-up page.

#     GET requests serve sign-up page.
#     POST requests validate form & user creation.
#     """
#     try:
        
#         form = SignupForm()
#         if form.validate_on_submit():
#             #check if user email is already occupied by an existing user 
#             existing_user = User.query.filter_by(email=form.email.data).first()
#             #inserting data into database via ORM User model models.py
#             if existing_user is None:
#                 user = User(
#                     username=form.username.data,
#                     email=form.email.data,
#                     appid=form.appid.data,
#                     created_on = dt.now(),
#                     admin=False,
#                 )
#                 user.set_password(form.password.data)
#                 db.session.add(user) #Staging the new user to be added to database
#                 db.session.commit()  # Create new user and adds it to the database
#                 login_user(user)  # Log in as newly created user
#                 # return redirect(url_for('main_bp.dashboard'))
#             return redirect(url_for('main.app_1_template'))
#             flash('A user already exists with that email address.')
#         return render_template(
#             'signup.html',
#             title='Create an Account.',
#             form=form,
#             template='signup-page',
#             body="Sign up for a user account."
#         )
#         pass
    
#     except IntegrityError as e:
#         return handle_integrity_error(e)


@auth_bp.errorhandler(404)
def page_not_found(e):
    print('hoho')
    # return render_template('404.html'), 404
    return "Hello" 



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    print("currentuser",current_user.get_id())
    # Bypass login process if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.app_1_template'))
    
    # login process
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email==form.email.data).first()
        
        print("USERRRR",user)
        #check_password is a function defined in model,py file
        if user and user.check_password(password==form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            # REturning to the Dash App after the successfull login
            return redirect(next_page or url_for('main.app_1_template'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )

# Returning back to home page flask
@auth_bp.route('/app_1_raw_dash/logout/')
@auth_bp.route('/app_2_raw_dash/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))  # Return back to main page flask

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
