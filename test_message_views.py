"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
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

        self.client = app.test_client()
    
    def tearDown(self):
    
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

    def test_add_message(self):
        """Can user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_delete_message(self):
        """Can user delete a message?"""

        message = Message(
            text = "Test message here",
            user_id = self.user.id
        )
        db.session.add(message)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            msg = Message.query.first()
            resp = c.post(f"/messages/{msg.id}/delete")

            self.assertEqual(resp.status_code, 302)

            msg = Message.query.first()
            self.assertIsNone(msg)

    def test_add_message_logged_out(self):
        """Can user add a message when logged out?"""


        with self.client as c:
            # with c.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.user.id

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn('Access unauthorized', html)


    def test_follow_pages(self):
        """Can we see follow page for a user when logged in"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/following")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Follow', html)
    
    def test_follow_pages_not_logged_in(self):
        """Do we get redirected when not logged in"""

        with self.client as c:
            # with c.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/following",follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn('Access unauthorized', html)
    
    def add_message_as_another_user(self):
        """Are you prohibited from adding a message another user"""

        user2 = User.signup(
            username="testuser2",
            email="test@test2.com",
            password="pass123",
            image_url= User.image_url.default.arg
        )
        db.session.add(user2)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = user2.id

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn('Access unauthorized', html)
    
    def delete_message_as_another_user(self):
        """Are you prohibited from adding a message another user"""

        user2 = User.signup(
            username="testuser2",
            email="test@test2.com",
            password="pass123",
            image_url= User.image_url.default.arg
        )
        db.session.add(user2)
        db.session.commit()

        message = Message(
            text = "Test message here",
            user_id = self.user.id
        )
        db.session.add(message)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = user2.id

            resp = c.post("f"/messages/{msg.id}/delete, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn('Access unauthorized', html)
    


    

        

    
