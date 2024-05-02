import unittest
from flask_testing import TestCase
from app import *


class TestRegistration(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration_success(self):
        response = self.client.post('/register', data=dict(
            username='test_user',
            password='test_password'
        ), follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_registration_username_taken(self):
        user = User(username='existing_user', password='existing_password')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/register', data=dict(
            username='existing_user',
            password='test_password'
        ), follow_redirects=True)
        self.assertIn(b'Username is taken', response.data)

class TestLogin(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        user = User(username='test_user', password='hashed_password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        response = self.client.post('/login', data=dict(
            username='test_user',
            password='hashed_password'
        ), follow_redirects=True)
        self.assertIn(b'Success', response.data)

    def test_login_invalid_password(self):
        response = self.client.post('/login', data=dict(
            username='test_user',
            password='wrong_password'
        ), follow_redirects=True)
        self.assertIn(b'Wrong Password', response.data)

if __name__ == '__main__':
    unittest.main()
