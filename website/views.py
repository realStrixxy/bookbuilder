from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from sqlalchemy import and_
from . import ai
import json, yaml
from .models import User, Book
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
    if 'id' in request.args.to_dict():
        book1 = Book.query.filter_by(id=int(request.args.to_dict()['id'])).first()
        session.clear()
        session['bookId'] = book1.id

        return render_template('book.html', book=book1.data, yes=True, user=current_user) 
    else:
        misc = yaml.load(current_user.misc, Loader=yaml.Loader)
        ai1 = ai.AI(misc['api-key'], misc['model'])
        book = ai1.WriteBook(session['sys'], session['topic'], int(session['chapters']), int(session['topics']))
        if book[1] == False:
            flash("Unable to generate response.", 'error')
        elif book[1] == True:
            flash("Successfully generated.", 'success')
            newBook = Book(user_id=current_user.id, title=book[2], data=book[0], misc='{}')
            db.session.add(newBook)
            db.session.commit()

        return render_template('book.html', book=book[0], yes=False, user=current_user) 

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/delete-book', methods=['GET'])
@login_required
def deleteBook():
    bookId = session['bookId']

    book1 = Book.query.filter_by(id=int(bookId)).first()
    session.clear()

    if current_user.id != book1.user_id:
        flash("You cannot delete another user's book.", 'error')
    else:
        db.session.delete(book1)
        db.session.commit()
        flash("Successfully deleted book.", 'success')

    return redirect(url_for('views.home'))