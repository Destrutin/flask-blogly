import unittest
from flask import Flask
from app import app, db
from models import connect_db, User, Post

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://destrutin/blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class FlaskTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_redirect_to_users(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  
        
    def test_list_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add user', response.data)
        self.assertIn(b'<h1>Blogly</h1>', response.data)

    def test_show_user(self):
        with app.app_context():
            user = User(first_name = 'Fang', last_name = 'boi', image_url = 'https://img.icons8.com/?size=256&id=tZuAOUGm9AuS&format=png')
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fang boi', response.data)

    
    def test_add_post(self):
        with app.app_context():
            user = User(first_name='Fang', last_name='Boi', image_url='https://img.icons8.com/?size=256&id=tZuAOUGm9AuS&format=png')
            db.session.add(user)
            db.session.commit()

            response = self.app.post(f'/users/{user.id}/posts/new', data={'title': 'Test Post', 'content': 'Test Content'})
            self.assertEqual(response.status_code, 302)  

    def test_edit_post(self):
        with app.app_context():
            user = User(first_name='Fang', last_name='Boi', image_url='https://img.icons8.com/?size=256&id=tZuAOUGm9AuS&format=png')
            db.session.add(user)
            db.session.commit()

            post = Post(title='Old Title', content='Old Content', user=user)
            db.session.add_all([user, post])
            db.session.commit()

            with app.test_client() as client:
                client.post(f'/posts/{post.id}/edit', data={'title': 'New Title', 'content': 'New Content'})

            post = Post.query.filter_by(id=post.id).first()
            
            self.assertEqual(post.title, 'New Title')  

    def test_show_post_details(self):
        with app.app_context():
            user = User(first_name='Fang', last_name='Boi', image_url='https://img.icons8.com/?size=256&id=tZuAOUGm9AuS&format=png')
            db.session.add(user)
            db.session.commit()

            post = Post(title='Test Post', content='Test Content', user=user)
            db.session.add(post)
            db.session.commit()

            post = Post.query.filter_by(id=post.id).first()
            response = self.app.get(f'/posts/{post.id}')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()