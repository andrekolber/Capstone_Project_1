"""SQLAlchemy models"""

from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    tracked_stocks = db.relationship("TrackedStock", backref="user")

    @classmethod
    def signup(cls, username, password, email, first_name, last_name):
        """Sign Up a new user and Hash password to database"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with username and password"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class Stock(db.Model):
    """Stock Model"""

    __tablename__ = 'stocks'

    symbol = db.Column(db.Text, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    exchange = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)


class TrackedStock(db.Model):
    """User Tracked Stock Model"""

    __tablename__ = 'tracked_stocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)

    stock_symbol = db.Column(db.Text, nullable=False, unique=False)





