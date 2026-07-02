from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, Tag
from . import db
import json

#creates a new page
views = Blueprint('views', __name__)

#now only looking at the board (creating a post should be separate)
@views.route('/', methods=['GET'])
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("home.html", user=current_user, posts=posts, tags=tags)

#create new post
@views.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        category = request.form.get('category')
        location_city = request.form.get('location_city')
        location_zip = request.form.get('location_zip')
        location_name = request.form.get('location_name')
        event_date = request.form.get('event_date') or None
        event_day = request.form.get('event_day')
        event_time = request.form.get('event_time') or None
        is_recurring = request.form.get('is_recurring') == 'on'
        instagram_url = request.form.get('instagram_url')
        group_chat_url = request.form.get('group_chat_url')
        contact_email = request.form.get('contact_email')
        tag_names = request.form.get('tags', '').split(',')
        if len(title) < 2:
            flash('Title is too short.', category='error')
        else:
            new_post = Post(title=title, 
                            body=body, 
                            category=category,
                            location_city=location_city, 
                            location_zip=location_zip,
                            location_name=location_name, 
                            event_date=event_date,
                            event_day=event_day, 
                            event_time=event_time,
                            is_recurring=is_recurring, 
                            instagram_url=instagram_url,
                            group_chat_url=group_chat_url, 
                            contact_email=contact_email,
                            user_id=current_user.id)
        #look up tags to see if included
        for name in tag_names:
            name = name.strip().lower()
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                new_post.tags.append(tag)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created!', category='success')
        return redirect(url_for('views.home'))

    return render_template('create.html', user=current_user)

@views.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
    data = json.loads(request.data)
    postId = data['postId']
    post = Post.query.get(postId)
    if post and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    #turn empty python into json object to return 
    return jsonify({})

@views.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    #looks up note by id to make sure it exists
    post = Post.query.get_or_404(id)

    if post.user_id != current_user.id:
        flash("You are not authorized to edit this note.", category='error')
        return redirect(url_for('views.home'))

    #submitted form to edit post
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        post.category = request.form.get('category')
        post.location_city = request.form.get('location_city')
        post.location_zip = request.form.get('location_zip')
        post.location_name = request.form.get('location_name')
        post.event_date = request.form.get('event_date') or None
        post.event_day = request.form.get('event_day')
        post.event_time = request.form.get('event_time') or None
        post.is_recurring = request.form.get('is_recurring') == 'on'
        post.instagram_url = request.form.get('instagram_url')
        post.group_chat_url = request.form.get('group_chat_url')
        post.contact_email = request.form.get('contact_email')
        tag_names = request.form.get('tags', '').split(',')
        post.tags = []
        for name in tag_names:
            name = name.strip().lower()
            if name:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                post.tags.append(tag)
        db.session.commit()
        flash("Post updated!", category='success')
        return redirect(url_for('views.home'))
    
    tag_string = ','.join(t.name for t in post.tags)
    return render_template('edit_post.html', user=current_user, post=post, tag_string=tag_string)

