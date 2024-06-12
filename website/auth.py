from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        apikey = request.form.get('apikey')
        model = request.form.get('models')

        user = User.query.filter_by(username=username).first()
        user2 = User.query.filter_by(email=email).first()
        if user:
            flash('Username already exists.', category='error')
        if user2:
            flash('Email already exists.', category='error')
        elif len(name) > 100:
            flash('Name too long.', 'error')
        elif len(username) < 4:
            flash('Username too short.', 'error')
        elif len(username) > 20:
            flash('Username too long.', 'error')
        elif len(email) < 4:
            flash('Email too short.', 'error')
        elif len(password) < 4:
            flash('Password too short.', 'error')
        elif len(password) > 20:
            flash('Password too long.', 'error')
        else:
            newUser = User(name=name, username=username, password=generate_password_hash(password, method='scrypt'), email=email, misc=str({"api-key": apikey, "model": model}))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('Account created.', 'success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login success.', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', 'error')
        else:
            flash('User does not exist.', 'error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))