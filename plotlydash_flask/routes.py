"""Routes for parent Flask app."""
# import flask
from flask import render_template, url_for, redirect, make_response, request, Blueprint,session
from forms import ContactForm, VerifyForm
from models import db, User
from datetime import datetime as dt
# from werkzeug.wsgi import DispatcherMiddleware
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_login import login_required
from flask_mail import Message
from extensions import mail
# from random import *
import random as rand


# Blueprint Configuration
main_bp = Blueprint(
    'main',                 #We have given new name to this Blueprint just for fun
    __name__,
    template_folder='templates',
    static_folder='static'
)

#-----------------------------------------------------------
# Home page Dash within Flask
# Main Route to access Dash App within Flask
# "/app_1_raw_dash is base pathname defined in auth.py
# The authentication is performed in callbacks.py NOT here
#-----------------------------------------------------------
@main_bp.route('/retail')  # this end point name 
@login_required
def app_1_template():
    print("y6")
    # if current_user.is_authenticated:
    return redirect('/demo1/')   #base_pathname in init.py file

#-----------------------------------------------------------
# Home page Dash within Flask
# Main Route to access Dash App within Flask
# "/app_1_raw_dash is base pathname defined in auth.py
# The authentication is performed in callbacks.py NOT here
#-----------------------------------------------------------
@main_bp.route('/media')  # this end point name 
@login_required
def app_2_template():
    print("y66")
    # if current_user.is_authenticated:
    return redirect('/demo2/')   #base_pathname in init.py file



# Home page FLASK
@main_bp.route('/')
@main_bp.route('/home')
def home():
    print("y5")
    """Landing page."""
    return render_template(
        'home1.html',
        title='Data Analytics Demo',
        description='Live Demo of data analytics',
        template='home-template',
        body="This is a homepage."
    )

@main_bp.route('/video')
def display_video():
	#print('display_video filename: ' + filename)
	return render_template('hero1.html',filename='/static/video/demo_video1.mp4')



# Contact Forms route
# Retrive and save info from the contact form and
# Sending OTP to the visitor email
@main_bp.route("/contact", methods=["GET","POST"])
def contact():

    """Standard `contact` form."""
    # Create form object instance
    form = ContactForm()
    # validate on form submit
    if form.validate_on_submit():
        # Generate OTP
        otp = rand.randint(000000,999999)

        # Preparing Email to be sent on Form submission
        # Check if method is post then copy submitted form elements into variables
        if request.method=="POST":
            name=request.form.get('name')
            email=request.form.get('email')
            company=request.form.get('company')
            message=request.form.get('body')

            # Store variables into seaaion vars to be used in next route
            session['name']= name
            session['email']= email
            session['company']= company
            session['message']= message
            session['otp']= otp

            # Sending OTP to the visitor
            msg = Message(
                subject="OTP",body=str(otp),sender= '66mufti@gmail.com',recipients=[email]
                )
            # send email
            mail.send(msg)

        return redirect(url_for('main.verify'))

    return render_template(
        "contact.html",
        form=form,
        template="form-template"
    )


# New view with input field for entering the OTP received in visitor email
# The OTP entered is verified with the OTP global var and if successful a mail to myself is send
@main_bp.route("/verify", methods=["GET", "POST"])
def verify():
    """Mail Verification of OTP"""
    # Create form object instance
    form = VerifyForm()

    # Retrieving stored form inputs from session variables
    name=session.get('name')
    email=session.get('email')
    company=session.get('company')
    message=session.get('message')
    otp=session.get('otp')

    # validate on form submit
    if form.validate_on_submit():
        # Preparing Email to be sent on Form submission
        # Check if method is post then copy submitted form elements into variables
        if request.method=='POST':
            user_otp=request.form.get('otp')

            if otp == int(user_otp):
                # Sending mail to myself after the verification is done successfully
                msg1 = Message(
                    subject=f"Mail from {name}",body=f"Name: {name}\nE-Mail: {email}\nCompany: {company}\n\nMessage :{message}",sender= 'doesnotmatter@hotmail.com',recipients=['66mufti@gmail.com']
                    )

                mail.send(msg1)

                ## Now build email subject and body messages to be sent
                # msg2 = Message(
                #     subject=f"Mail from {name}",body=f"Name: {name}\nE-Mail: {email}\nCompany: {company}\n\nMessage :{message}",sender= '66mufti@gmail.com',recipients=['mmufti@hotmail.com']
                #     )
                # # send email
                # mail.send(msg2)

                return render_template( "success.html",name=name,mail=email)


            else:
                return render_template( "fail.html",name=name,mail=email)

    return render_template( "verify.html",form=form,name=name,mail=email)


# Successful form entry Page
@main_bp.route('/success')
def success():
    return render_template(
        'success.html'
        )

#-------------------------------------------------------------------------
# User entry in Database using URL query string
# Example adding user and email using URL:
# http://127.0.0.1:5000/users?user=mubashir&email=mmufti@hotmail.com
#-------------------------------------------------------------------------
@main_bp.route('/users', methods=['GET'])
def user_records():
    """Create a user via query string parameters.
    request.args.get fetches  the URL parameters after ? """
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(
                f'{username} ({email}) already created!'
            )
        new_user = User(
            username=username,
            email=email,
            created_on=dt.now(),
            bio="In Lahore born and raised in Karachi, \
            on the playground is where I spent most of my days",
            # admin=False
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return render_template(
        'users.html',
        users=User.query.all(),
        title="Show Users",
    )

#----------------------------------------------
# SECURING direct routes entered in browser
#Implmenting Authentication for the DASH pages other then Main
# to restrict direct access to the url
#----------------------------------------------
#PLot page
@main_bp.route('/demo1/demo1/pages/plot')
@login_required
def plot_for_loggedin():
    return redirect(url_for('main.app_1_template'))

#Reports generation page
@main_bp.route('/demo1/demo1/pages/report')
@login_required
def report_for_loggedin():
    return redirect(url_for('main.app_1_template'))

#Reports viewer Page
@main_bp.route('/demo1/demo1/pages/table')
@login_required
def table_for_loggedin():
    return redirect(url_for('main.app_1_template'))


