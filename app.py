"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for
from models import db, connect_db, User, default_image_url, Post
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://destrutin:Chainsaw5@localhost:5432/blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)


with app.app_context():
    db.create_all()


@app.route('/')
def redirect_to_users():
    """Redirect to the list of users."""

    users = User.query.all()
    
    for user in users:
        if user.image_url:
            try:
                response = requests.get(user.image_url)
                response.raise_for_status()  
            
            except requests.RequestException as e:
                # If an exception occurs, redirect to the default URL
                print(f"Error: {e}")
                user.image_url = default_image_url
        else:
            user.image_url = default_image_url

    db.session.commit()

    return render_template('users/users.html', users=users)

@app.route('/users')
def list_users():
    """Show list of users."""

    users = User.query.all()
    return render_template('users/users.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Show the add user form."""
    
    return render_template('users/add_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Process the add form, adding a new user."""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('list_users'))  

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('users/user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Show the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Process the edit form, updating the user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Show form to add a post for a user."""
    user = User.query.get_or_404(user_id)
    return render_template('posts/add_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user = User.query.get_or_404(user_id)

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('show_user', user_id=user_id))

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('posts/post_details.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()

    return redirect(url_for('show_post', post_id=post_id))

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('show_user', user_id=post.user_id))

if __name__ == '__main__':
    app.run(debug = True)