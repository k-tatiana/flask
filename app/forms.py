from flask_wtf import FlaskForm
from wtforms import (BooleanField,
                     StringField,
                     PasswordField,
                     SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class EditProfileForm(FlaskForm):
    userEdit = StringField('Пользователь:', validators=[DataRequired()])
    aboutEdit = TextAreaField('Обо мне:', validators=[Length(max=140)])
    submitEdit = SubmitField('Сохранить')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Используйте другое имя пользователя.')

class LoginForm(FlaskForm):
    username2 = StringField('Пользователь:', validators=[DataRequired()])
    password2 = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me2 = BooleanField('Запомнить', default=False)
    submit2 = SubmitField('Вход')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    passwordCheck = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_user(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Данное имя пользователя уже существует, выберите другое')

    def validate_mail(self, email):
        mail = User.email.filter_by(email = email.data).first()
        if mail is not None:
            raise ValidationError('Данная почта уже используется')



