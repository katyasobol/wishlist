from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError, FileField, FloatField, URLField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
import re

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите свой юзернейм"}, name='username')
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": " Введите пароль"}, name='psw')
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите свой юзернейм"}, name='username')
    email = EmailField(validators=[Email(message='Некорректный email')], render_kw={"placeholder": "Введите свой email"}, name='email')
    psw = PasswordField(validators=[InputRequired()], render_kw={"placeholder": " Введите пароль"}, name='psw')
    psw2 = PasswordField(validators=[InputRequired(), EqualTo('psw', message="Пароли не совпадают")], render_kw={"placeholder": "Повторите пароль"})
    firstname = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": "Введите имя"}, name='firstname')
    lastname = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": "Введите Фамилию"}, name='lastname')
    birthdate = StringField(validators=[InputRequired(), Length(max=10), Regexp(r'\d\d.\d\d.\d{4}', message='Дата вида дд.мм.гггг')], render_kw={"placeholder": "Введите дату рождения"}, name='birthdate')
    img = FileField(name='img', id='file-input')
    submit = SubmitField("Зарегистрироваться")

class PostForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(max=20)], name='title')
    price = FloatField(name='price')
    comment = StringField(name='comment')
    url = URLField(name='url')
    img = FileField(name='img', id='file-input')
    submit = SubmitField("Сохранить")

class BookForm(FlaskForm):
    name = StringField(render_kw={"placeholder": "Введите свое имя"}, name='name')
    email = EmailField(validators=[Email(message='Некорректный email')], render_kw={"placeholder": "Введите свой email"}, name='email')
    book = BooleanField()
    submit = SubmitField("Забронировать")

def validate_date(field):
        if re.fullmatch(field, r'\d\d\.\d\d\.\d{4}'):
            raise ValidationError('дата формата дд,мм.гггг')
        return True

def verify_img(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in ALLOWED_EXTENSIONS:
        return True
    return False
