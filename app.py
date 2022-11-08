from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/wishlistsql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdgfh78@#5?>gfhf89dx,v06'
app_context = app.app_context()
app_context.push()

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    psw = db.Column(db.String(200), nullable=False)
    birthdate = db.Column(db.DateTime)
