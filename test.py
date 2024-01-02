import unittest
from flask import Flask
from app import app, db
from models import connect_db, User, Post, Tag, PostTag

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

# Test Users --------------------------------------------

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

# Test Posts ---------------------------------
    
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

# Test Tags ---------------------------------
            
    def test_list_tags(self):
        response = self.app.get('/tags')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add tag', response.data)
        self.assertIn(b'<h1>Tags</h1>', response.data)

    def test_show_tag(self):
        with app.app_context():
            tag = Tag(name='Test Tag')
            db.session.add(tag)
            db.session.commit()
            tag_id = tag.id

        response = self.app.get(f'/tags/{tag_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Tag', response.data)

    def test_add_tag(self):
        with app.app_context():
            tag_name = 'New Tag'
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.commit()

            tags = Tag.query.all()
            self.assertEqual(len(tags), 1)
            self.assertEqual(tags[0].name, tag_name)

    def test_edit_tag(self):
        with app.app_context():
            user = User(first_name='Fang', last_name='Boi', image_url='https://img.icons8.com/?size=256&id=tZuAOUGm9AuS&format=png')
            db.session.add(user)
            db.session.commit()

            post = Post(title='Test Post', content='Test Content', user=user)
            db.session.add(post)
            db.session.commit()

            tag = Tag(name='Old Tag')
            db.session.add(tag)
            db.session.commit()

            post_tag = PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(post_tag)
            db.session.commit()

            response = self.app.post(f'/tags/{tag.id}/edit', data={'name': 'Updated Tag'})
            self.assertEqual(response.status_code, 302)  

            updated_tag = Tag.query.get(tag.id)
            self.assertEqual(updated_tag.name, 'Updated Tag')

    def test_delete_tag(self):
        with app.app_context():
            tag = Tag(name='Tag to be deleted')
            db.session.add(tag)
            db.session.commit()

            response = self.app.post(f'/tags/{tag.id}/delete')
            self.assertEqual(response.status_code, 302)  
            tags = Tag.query.all()
            self.assertEqual(len(tags), 0)

if __name__ == '__main__':
    unittest.main()