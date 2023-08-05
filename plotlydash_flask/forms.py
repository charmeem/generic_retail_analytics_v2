from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField,PasswordField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,Length,Optional

class VerifyForm(FlaskForm):
    otp = IntegerField(
        'Enter OTP (One time password)',
        [
            DataRequired()
        ]
    )
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'FullName',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ]
    )
    company = StringField(
        'Company Name',
        [
            DataRequired()
        ]
    )
    
    body = StringField(
        'Write Message e.g. Send me login password',
        [
            DataRequired(),
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
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    website = StringField(
        'Website',
        validators=[Optional()]
    )
    
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()
        ]
       )
    
    submit = SubmitField('Log In')