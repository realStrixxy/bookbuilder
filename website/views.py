from flask import Blueprint, render_template, request, flash, url_for, redirect
from . import ai

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        topic = request.form.get('topic')
        chapters = request.form.get('chapters')
        topics = request.form.get('topics')
        return redirect(f'/book?topic={topic}&chapters={chapters}&topics={topics}')

    return render_template('home.html')

@views.route('/book', methods=['GET'])
def book():
    bookInfo = request.args.to_dict()
    book = ai.WriteBook(bookInfo['topic'], int(bookInfo['chapters']), int(bookInfo['topics']))

    return render_template('book.html', book=book)