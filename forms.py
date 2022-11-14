from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите свой юзернейм"}, name='username')
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": " Введите пароль"}, name='psw')
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите свой юзернейм"}, name='username')
    email = EmailField(validators=[Email(message='Некорректный email')], render_kw={"placeholder": "Введите свой email"}, name='email')
    psw = PasswordField(validators=[InputRequired()], render_kw={"placeholder": " Введите пароль"}, name='psw')
    psw2 = PasswordField(validators=[InputRequired(), EqualTo('psw', message="Пароли не совпадают")], render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField("Зарегистрироваться")

class ProfileForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите имя"}, name='firstname')
    lastname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите Фамилию"}, name='lastname')
    birthdate = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Введите дату рождения"}, name='birthdate')
    submit = SubmitField("Изменить")