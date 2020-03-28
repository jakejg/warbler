"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        
        self.user = User.signup(
            username="testuser",
            email="test@test.com",
            password="pass123",
            image_url= User.image_url.default.arg
        )
        self.user2 = User.signup(
            username="testuser2",
            email="test2@test.com",
            password="lkjdsk",
            image_url = User.image_url.default.arg
        )
        db.session.add_all([self.user, self.user2])
        db.session.commit()

        self.client = app.test_client()
    
    def tearDown(self):
    
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()
        

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.user.messages), 0)
        self.assertEqual(len(self.user.followers), 0)

    def test_repr(self):
        """Test repr"""

        self.assertEqual(str(self.user), f'<User #{self.user.id}: testuser, test@test.com>')
    
    def test_is_following(self):
        """Test that self.user can follow and unfollow user2"""

        # follow
        self.user.following.append(self.user2)
        db.session.commit()

        self.assertEqual(self.user.following[0], self.user2)

        # unfollow
        self.user.following.remove(self.user2)
        db.session.commit()

        self.assertEqual(len(self.user.following), 0)    

    def test_is_followed_by(self):
        """Test that self.user can be followed and unfollowed by user2"""

        # follow
        self.user.followers.append(self.user2)
        db.session.commit()

        self.assertEqual(self.user.followers[0], self.user2)

        # unfollow
        self.user.followers.remove(self.user2)
        db.session.commit()

        self.assertEqual(len(self.user.followers), 0)  

    def test_create_user_good(self):
        """Test a correct user signup"""

        new_user = User.signup(
            username="test3",
            password="lkjklj",
            email="test3@test.com",
            image_url=User.image_url.default.arg)

        db.session.add(new_user)
        db.session.commit()

        new_user_from_database = User.query.filter_by(username="test3").first()
        self.assertEqual(new_user, new_user_from_database)
    
    def test_create_user_bad(self):
        """Test a user signup with duplicate username"""
        try:
            new_user = User.signup(
                username="testuser",
                password="oijdssdf",
                email="t@t.com",
                image_url=User.image_url.default.arg)

        except IntegrityError:
            self.assertIsNone(new_user)

    def test_authenticate_user_good(self):
        """Test login with a valid username and password"""

        logged_in_user = User.authenticate("testuser", "pass123")
        self.assertTrue(logged_in_user)
        self.assertEqual(logged_in_user.username, "testuser" )

    def test_authenticate_user_bad_username(self):
        """Test login with a invalid username"""

        logged_in_user = User.authenticate("testuserbad", "pass123")
        self.assertFalse(logged_in_user)

    def test_authenticate_user_bad_password(self):
        """Test login with a invalid passowrd"""

        logged_in_user = User.authenticate("testuser", "pass1234toomany")
        self.assertFalse(logged_in_user)
        
    
    

    


       
        




        


    

