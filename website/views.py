from flask import Blueprint, render_template, request, flash, url_for, redirect
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
        topic = request.form.get('topic')
        chapters = request.form.get('chapters')
        topics = request.form.get('topics')
        return redirect(f'/book?topic={topic.replace(" ", "%20")}&chapters={chapters}&topics={topics}')

    return render_template('home.html', user=current_user)

@views.route('/book', methods=['GET'])
@login_required
def book():
    bookInfo = request.args.to_dict()
    book = ai.WriteBook(bookInfo['topic'], int(bookInfo['chapters']), int(bookInfo['topics']))

    return render_template('book.html', book=book, user=current_user) 