"""Data models."""
# from . import db
import sys
# sys.path.append('plotlydash_flask')
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin,db.Model):
    """Data model for user accounts."""

    __tablename__ = 'piesis-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    appid = db.Column(
        db.Integer,
        unique=False,
        primary_key=False,
        nullable=False
    )
    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
        )
    
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='pbkdf2:sha256'
        )
        
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)    

    def __repr__(self):
        return '<User {}>'.format(self.username)


    