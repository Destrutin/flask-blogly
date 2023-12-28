"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://destrutin/blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)

@app.route('/')
def redirect_to_users():
    """Redirect to the list of users."""
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users')
def list_users():
    """Show list of users."""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Show the add user form."""
    
    return render_template('add_user.html')

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
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Show the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)