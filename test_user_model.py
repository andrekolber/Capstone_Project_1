"""User Model Tests"""

import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, User, TrackedStock

os.environ['DATABASE_URL'] = "postgresql:///stock-portal-test"
from app import app
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False




class UserModelTestCase(TestCase):
    """Test User Model"""
    def setUp(self):
        """Create test client."""

        db.drop_all()
        db.create_all()

        user = User.signup(
            username="test",
            password="password",
            first_name="First",
            last_name="Last",
            email="test@test.com"
        )

        user.id = 123
        
        db.session.commit()

        user = User.query.get(user.id)

        self.user = user
        self.user.id = user.id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    
    def test_user_model(self):
        """Test basic model"""

        user = User(
            username="test1",
            password="password1",
            first_name="First1",
            last_name="Last1",
            email="test1@test.com"
        )

        db.session.add(user)
        db.session.commit()

        self.assertTrue(User.query.filter_by(username="test1"))
        self.assertTrue(User.query.filter_by(email="test1@test.com"))
        self.assertTrue(User.query.filter_by(first_name="First1"))
        self.assertTrue(User.query.filter_by(last_name="Last1"))
        self.assertFalse(user.tracked_stocks)

    
    def test_valid_signup(self):
        u_test = User.signup("testtest", "testpassword", "test1@test.com", "First", "Last")
        uid=11111
        u_test.id=uid
        db.session.commit()

        u_test=User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtest")
        self.assertEqual(u_test.email, "test1@test.com")
        self.assertNotEqual(u_test.password, "password")
        self.assertTrue(u_test.password.startswith("$2b$"))


    def test_invalid_username_signup(self):
        invalid = User.signup(None, "testpassword", "test@test.com", "First", "Last")
        uid = 123123123
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", "testpassword", None, "First", "Last")
        uid = 456456456
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "", "test@test.com", "First", "Last")

        with self.assertRaises(ValueError) as context:
            User.signup("testtest", None, "test@test.com", "First", "Last")


    def test_valid_authentication(self):
        u = User.authenticate(self.user.username, "password")
        self.assertIsNotNone(u)

    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("notausername", "password"))


    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.user.username, "notapassword"))


    



        



    