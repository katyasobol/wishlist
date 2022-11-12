from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from database import User, Profile
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, login_required
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10122000kot@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdgfh78@#6?>gfhf80dx,v06'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return user_id

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

        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация')

@app.route('/profile', methods=('POST', 'GET'))
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', title='Профайл')
    return redirect(url_for('login'))


@app.route('/profile/update', methods=('POST', 'GET'))
@login_required
def update():
    if request.method == "POST":
        try:
            p = Profile(firstname=request.form['firstname'], lastname=request.form['lastname'], birthdate=request.form['birthdate'])
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
        return redirect(url_for('profile'))
    return render_template('profileupd.html', title='Настройки аккаунта')


@app.route('/login', methods=('POST', 'GET')) 
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        psw = request.form.get('psw')
        if username == User.query.get(0) and check_password_hash(psw, User.psw.get(username.id)):
            return redirect(url_for('profile'))
        flash("Неверная пара логин/пароль", "error")
    return render_template('login.html')      

if __name__ == '__main__':
    app.run(debug=True)

