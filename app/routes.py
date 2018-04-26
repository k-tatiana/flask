from app import app, db
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'nickname': 'Miguel'}
    posts = [  # список выдуманных постов
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           posts=posts)


@app.route('/hello')
def hello():
    return "Hello, you too!"


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(name=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}]
    return render_template('user.html', user=user, posts=posts)


@app.route('/post/<int:post_id>')
@login_required
def show_post(post_id):
    return 'Post № %d' % post_id


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username2.data).first()
        if user is None or not user.check_password(form.password2.data):
            flash('Wrong user or pass, try again to Sign In')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me2.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign me In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, Вы зарегистрировались как новый пользователь')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Зарегистрироваться', form=form)
