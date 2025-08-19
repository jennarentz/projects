from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#creates a new page
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    #turn empty python into json object to return 
    return jsonify({})

@views.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    #looks up note by id to make sure it exists
    note = Note.query.get_or_404(id)

    if note.user_id != current_user.id:
        flash("You are not authorized to edit this note.", category='error')

    #submitted form to edit note
    if request.method == 'POST':
        new_text = request.form.get('note')
        if len(new_text) < 1:
            flash("Note can't be empty.", category='error')
        else:
            note.text = new_text
            db.session.commit()
            flash("Note updated!", category='success')

    return render_template('edit_note.html', user=current_user, note=note)

