import flask
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from forms import LoginForm, SignupForm
from models import db, User
# from . import login_manager
from extensions import login_manager
# from . import login_manager

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
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                username=form.name.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            # return redirect(url_for('main_bp.dashboard'))
        return redirect(url_for('main.app_1_template'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


# @auth_bp.errorhandler(404)
# def page_not_found(e):
#     print('hoho')
#     # return render_template('404.html'), 404
#     return "Hello" 



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.app_1_template'))
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
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

@auth_bp.route('/app_1_raw_dash/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

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
