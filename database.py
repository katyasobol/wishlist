from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10122000kot@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdgfh78@#5?>gfhf80dx,v06'
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
        return f'<user {self.id}>'


class Profile(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    birthdate = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, firstname, lastname, birthdate, user_id):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.user_id = user_id


    def __repr__(self):
        return f'<profile {self.id}>'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = User(user=request.form['username'], email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            return 'you ot registered'

        return render_template('login.html')
    return render_template('register.html', title='Регистрация')

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
