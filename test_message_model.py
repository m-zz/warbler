"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

""" Does the repr method work as expected?
Does is_following successfully detect when user1 is following user2?
Does is_following successfully detect when user1 is not following user2?
Does is_followed_by successfully detect when user1 is followed by user2?
Does is_followed_by successfully detect when user1 is not followed by user2?
Does User.signup successfully create a new user given valid credentials?
Does User.signup fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
Does User.authenticate successfully return a user when given a valid username and password?
Does User.authenticate fail to return a user when the username is invalid?
Does User.authenticate fail to return a user when the password is invalid? """


class MessageModelTestCase(TestCase):
    """Test model for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.u = u

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""

        user = User.query.get(username=self.u.username)

        m = Message(
            text="blah blah blah blah",
            user_id=user.id
        )

        db.session.add(m)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(type(m.timestamp), datetime)