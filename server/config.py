from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productApi.db'
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy()
bcrypt = Bcrypt(app)
