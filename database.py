from flask import Flask, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10122000kot@localhost/wishlistsql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdgfh78@#5?>gfhf89dx,v06'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    psw = db.Column(db.String(200), nullable=False)

    def __init__(self, user, email, psw):
        self.user = user
        self.email = email
        self.psw = psw
    
    def __repr__(self):
        return f'<users {self.id}'

db.init_app(app)
with app.app_context():
    db.create_all()




