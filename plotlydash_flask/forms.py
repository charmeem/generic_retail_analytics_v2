from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField,PasswordField,IntegerField,DateField, BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length,Optional,InputRequired

class VerifyForm(FlaskForm):
    otp = IntegerField(
        'Enter OTP (One time password)',
         validators=[InputRequired()]
        
    )
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'FullName',
        validators=[InputRequired()]
    )
    appid = IntegerField(
        'Appid',
        validators=[InputRequired()]
    )
    email = StringField(
        'Email',
        validators=
        [
            Email(message=('Not a valid email address.')),
            InputRequired()
        ]
    )
    company = StringField(
        'Company Name',
         validators=[InputRequired()]
        
    )
    
    body = StringField(
        'Write Message e.g. Send me login password',
        validators=
        [
            InputRequired(),
            Length(min=4,
            message=('Your message is too short.'),
            # placeholder="HI"
            ),            
        ]
    )
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
    
    

class SignupForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        'User Name',
        validators=[
                    InputRequired()
                    ]
    )
    appid = IntegerField(
        'Appid',
        validators=[InputRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            InputRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            InputRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    created_on = DateField(
        'Created on',
        validators=[Optional()]
    )
    admin = BooleanField(
        'Admin',
        validators=[Optional()]
    )
    
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[InputRequired()
        ]
       )
    
    submit = SubmitField('Log In')