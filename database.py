from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, RegisterForm, validate_date, verify_img, PostForm, BookForm
from base64 import b64encode, b64decode
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:10122000kot@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdgfh78@#5?>gfhf80dx,v06'
db = SQLAlchemy(app)
db.init_app(app)

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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Float)
    comment = db.Column(db.String(140))
    url = db.Column(db.String)
    img = db.Column(db.LargeBinary)

    def __init__(self, title, user_id, price, comment, url, img):
        self.title = title
        self.user_id = user_id
        self.price = price
        self.comment = comment
        self.url = url
        self.img = img
    
    def __repr__(self):
        return f'<post {self.id}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    book = db.Column(db.Boolean)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, name, email, book, post_id):
        self.name = name
        self.email = email
        self.book = book
        self.post_id = post_id
    
    def __repr__(self):
        return f'<post {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/wishlist', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit() and verify_img(request.files['img'].filename):
        try:
            hash = generate_password_hash(request.form['psw'])
            u = User(user=request.form['username'], email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()
            image = request.files['img']
            encode = b64encode(image.read()).decode('utf-8')
            p = Profile(firstname=request.form['firstname'], lastname=request.form['lastname'], birthdate=request.form['birthdate'], user_id=u.id, img=encode)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            return 'mistake'
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['POST', 'GET']) 
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
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

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = None
    if current_user.is_authenticated:
        image = None
        for raw in db.session.query(Profile).where(Profile.user_id == current_user.id):
                form = raw
                image = b64decode(form.img).decode('utf-8')
        return render_template('profile.html', form=form, image=image)
    return redirect(url_for('login'))  

@app.route('/profile/update', methods=['POST', 'GET'])
@login_required
def prof_upd():
    if request.method == 'POST':
        #print(b64encode(request.files['img'].read()).decode('utf-8'))
        try:
            for raw in db.session.query(Profile).where(Profile.user_id == current_user.id):
                user = raw
                user.firstname = request.form.get('firstname') if request.form.get('firstname') else user.firstname
                user.lastname = request.form.get('lastname') if request.form.get('lastname') else user.lastname
                user.birthdate = request.form.get('birthdate') if request.form.get('birthdate') and validate_date(request.form.get('birthdate')) else user.birthdate
                user.img = b64encode(request.files['img'].read()) if request.files['img'] else user.img
                db.session.commit()
                return redirect(url_for('profile'))
        except:
                db.session.rollback()
                return 'hrsghe'
        return redirect(url_for('profile'))
    return render_template('prof_upd.html')

@app.route('/newpost', methods=['POST', 'GET'])
@login_required
def post():
    form = PostForm()
    if request.method == "POST" and form.validate_on_submit() and verify_img(request.files['img'].filename):
        try:
            encode = b64encode(request.files['img'].read())
            p = Post(title=request.form['title'], price=request.form['price'], url=request.form['url'], img=encode, user_id=current_user.id, comment=request.form['comment'])
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            return 'mistake'
        return redirect(url_for('profile'))
    return render_template('post.html', form=form)

@app.route('/showpost/<int:post_id>', methods=['POST', 'GET'])
def showpost(post_id):
    form = None
    image = None
    book = None
    for raw in db.session.query(Post).where(Post.id == post_id):
        form = raw
        image = b64decode(form.img)
    return render_template('showpost.html', form=form, image=image, book=book)

    

@app.route('/posts/<int:post_id>', methods=['POST', 'GET'])
def posts(post_id):
    book = []
    raw = db.session.query(Post).where(Post.user_id == post_id)
    for p in db.session.query(Book).where(Book.book == True):
        book.append(p.post_id)
    return render_template('posts.html', form=raw, book=book)

@app.route('/post/update', methods=['POST', 'GET'])
@login_required
def post_upd():
    if request.method == 'POST':
        try:
            for raw in db.session.query(Post).where(Post.user_id == current_user.id):
                user = raw
                user.title = request.form.get('title') if request.form.get('title') else user.title
                user.price = request.form.get('price') if request.form.get('price') else user.price
                user.comment = request.form.get('comment') if request.form.get('comment') else user.comment
                user.url = request.form.get('url') if request.form.get('url') else user.url
                user.img = b64encode(request.files['img'].read()) if request.files['img'] else user.img
                db.session.commit()
                return redirect(url_for('profile'))
        except:
                db.session.rollback()
                return 'hrsghe'
        return redirect(url_for('profile'))
    return render_template('post_upd.html')

@app.route('/showpost/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete(post_id):
    try:
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('posts'))
    except:
        db.session.rollback()
        return 'mistake'

@app.route('/book/<int:post_id>', methods=['POST', 'GET'])
def book(post_id):
    form = BookForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            booked = True if request.form['book'] else False
            for raw in db.session.query(Post).where(Post.id == post_id):
                postid = raw.id
                p = Book(name=request.form['name'], email=request.form['email'], book=booked, post_id=postid)
                db.session.add(p)
                db.session.commit()
            return redirect(url_for('showpost', post_id=post_id))
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
            return 'mistake'
    return render_template('book.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

        