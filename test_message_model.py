"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.user = User.signup(
            username="testuser",
            email="test@test.com",
            password="pass123",
            image_url= User.image_url.default.arg
        )
        db.session.add(self.user)
        db.session.commit()
        
        self.message = Message(
            text = "Test message here",
            user_id = self.user.id
        )
        db.session.add(self.message)
        db.session.commit()

        self.client = app.test_client()
    
    def tearDown(self):
    
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()
        

    def test_message_model(self):
        """Does basic model work?"""

        # Message should have no likes & should have a relationship with the user that created it
        self.assertEqual(len(self.message.likes), 0)
        self.assertEqual(self.message.user, self.user)

    def test_like(self):
        """Test that a message can be liked"""
        like = Likes(user_id=self.user.id, message_id=self.message.id)
        db.session.add(like)
        db.session.commit()

        self.assertEqual(len(self.message.likes), 1)
        self.assertEqual(self.message.likes[0], like)
        self.assertEqual(self.message.user.likes[0], like)
    
    def test_unlike(self):
        """Test that a message can be unliked"""
        like = Likes(user_id=self.user.id, message_id=self.message.id)
        db.session.add(like)
        db.session.commit()

        like = Likes.query.get_or_404(like.id)
        db.session.delete(like)
        db.session.commit()

        self.assertEqual(len(self.message.likes), 0)
    
    def test_get_msg_ids(self):
        """Test get_msg_ids method"""

        message1 = Message(
            text = "Test message1 here",
            user_id = self.user.id
        )

        db.session.add_all([self.message, message1])
        db.session.commit()

        like = Likes(user_id=self.user.id, message_id=self.message.id)
        like1 = Likes(user_id=self.user.id, message_id=message1.id)

        db.session.add_all([like, like1])
        db.session.commit()

        messages = Message.query.all()

        msg_ids = Message.get_liked_msg_ids(messages)

        self.assertEqual(len(msg_ids), 2)
        self.assertIn(self.message.id, msg_ids)

        

    


       
        




        


    

