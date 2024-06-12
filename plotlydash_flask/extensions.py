# This file used to create instances of helper features like db, login, mails etc
 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail



db = SQLAlchemy()
login_manager = LoginManager() #NOTE: THIS VAR NAME MUST BE login_manager OTHERWISE IT WILL NOT WORK

mail = Mail()


