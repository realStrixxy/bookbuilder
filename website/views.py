from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from . import ai
from .models import User
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/home')
def reroute():
    return redirect(url_for('views.home'))

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        session.clear()
        session['sys'] = request.form.get('sys')
        session['topic'] = request.form.get('topic')
        session['chapters'] = request.form.get('chapters')
        session['topics'] = request.form.get('topics')

        return redirect(url_for('views.book'))

    return render_template('home.html', user=current_user)

@views.route('/book', methods=['GET'])
@login_required
def book():
    book = ai.WriteBook(session['sys'], session['topic'], int(session['chapters']), int(session['topics']))
    if book[1] == False:
        flash("Unable to generate response.", 'error')
    elif book[1] == True:
        flash("Successfully generated.", 'success')
    return render_template('book.html', book=book[0], user=current_user) 

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)