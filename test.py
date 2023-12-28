import unittest
from flask import Flask
from app import app, db
from models import connect_db, User

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://destrutin/blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

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
        self.assertIn('List of Users:', response.data)

    def test_list_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_show_user(self):
        with app.app_context():
            user = User(first_name = 'Fang', last_name = 'boi', image_url = 'https://icons8.com/icon/tZuAOUGm9AuS/user-default')
            db.session.add(user)
            db.session.commit()
        user_id = user.id
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()