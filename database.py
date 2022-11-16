from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, RegisterForm, ProfileForm, validate_date, binary_enc
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10122000kot@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdgfh78@#5?>gfhf80dx,v06'
db = SQLAlchemy(app)
db.init_app(app)

MAX_CONTENT_LENGTH = 1024 * 1024

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    psw = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return f'{self.id}'


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    birthdate = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img = db.Column(db.LargeBinary)

    def __init__(self, firstname, lastname, birthdate, user_id, img):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.user_id = user_id
        self.img = img

    def __repr__(self):
        return f'<profile {self.id}>'



with app.app_context():
    db.create_all()

@app.route('/wishlist', methods=['POST', 'GET'])
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hash = generate_password_hash(request.form['psw'])
            u = User(user=request.form['username'], email=request.form['email'], psw=hash)
            try:
                db.session.add(u)
                db.session.commit()
            except:
                db.session.rollback()
                print("Ошибка добавления в БД")
            return redirect(url_for('update'))
        flash('ошибка ввода данных')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/profile/<int:id>', methods=('POST', 'GET'))
@login_required
def profile():
    form = None
    if current_user.is_authenticated:
        for raw in db.session.query(Profile).where(Profile.user_id == current_user.id):
                form = raw
        return render_template('profile.html', title='Профайл', form=form)
    return redirect(url_for('login'))


@app.route('/register/update', methods=('POST', 'GET'))
def update():
    form = ProfileForm()
    if request.method == "POST":
        try:
            img = binary_enc(request.files['img'])
            print(img)
            p = Profile(firstname=request.form['firstname'], img=request.files['img'], lastname=request.form['lastname'], birthdate=request.form['birthdate'], user_id=current_user.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            return 'mistake'
        return redirect(url_for('profile'))
    return render_template('registerupd.html', title='Настройки аккаунта', form=form)

@app.route('/login', methods=('POST', 'GET')) 
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form.get('username')
            psw = request.form.get('psw')
            for raw in db.session.query(User).where(User.user == username):
                user = raw
            if username == user.user and check_password_hash(user.psw, psw):
                login_user(user=user)
                return redirect(url_for('profile'))
            flash("Неверная пара логин/пароль", "error")
    return render_template('login.html', form=form)  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))    

@app.route('/profile/update', methods=('POST', 'GET'))
@login_required
def prof_upd():
    if request.method == 'POST':
        if Profile.query.get(current_user.id):
            try:
                for raw in db.session.query(Profile).where(Profile.user_id == current_user.id):
                    user = raw
                    user.firstname = request.form.get('firstname') if request.form.get('firstname') else user.firstname
                    user.lastname = request.form.get('lastname') if request.form.get('lastname') else user.lastname
                    user.birthdate = request.form.get('birthdate') if request.form.get('birthdate') and validate_date(request.form.get('birthdate')) else user.birthdate
                    user.img = request.form.get('img') if request.form.get('img') else user.img
                    db.session.commit()
                    return redirect(url_for('profile'))
            except:
                    db.session.rollback()
                    return 'hrsghe'
        p = Profile(firstname=request.form['firstname'], lastname=request.form['lastname'], birthdate=request.form['birthdate'], user_id=current_user.id, img=request.form['img'])
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('prof_upd.html')


if __name__ == '__main__':
    app.run(debug=True)
