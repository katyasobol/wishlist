from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database import User, db

app = Flask(__name__)

@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = User(user=request.form['username'], email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('profile'))
    return render_template('register.html', title='Регистрация')

@app.route('/profile', methods=('POST', 'GET'))
def profile():
    return render_template('profile.html', title='Профайл')

if __name__ == '__main__':
    app.run(debug=True)

