"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False



class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_user_page(self):
        """Can see the user's page when logged in and out"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn("Following", html)
            self.assertIn("Followers", html)

            c.get('/logout', follow_redirects=True)
            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertNotIn("Following", html)
            self.assertNotIn("Followers", html)

    def test_add_delete_message(self):
        """Can you add and delete a message when logged in"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post('/messages/new', data={"text": "Hello"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Hello", html)

            msg = Message.query.one()
            del_route = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            html = del_route.get_data(as_text=True)

            self.assertNotIn("Hello", html)


    def test_add_delete_message_when_logged_out(self):
        """Can you add and delete a message when logged out"""

        with self.client as c:
            resp = c.get('/messages/new', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Access unauthorized", html)

            del_route = c.post(f"/messages/1/delete", follow_redirects=True)
            html = del_route.get_data(as_text=True)

            self.assertIn("Access unauthorized", html)


"""
When you’re logged in, are you prohibiting from adding a message as another user?
When you’re logged in, are you prohibiting from deleting a message as another user?
"""