from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
#import os

app = Flask(__name__)
#export VARIABLE=value---use this in the terminal
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@123.45.6.78:3306/mydatabase'
app.config['SECRET_KEY'] = 'bA5qzruPYLAyyx5QFNUVCg'

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'



from application import routes