"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

import sqlalchemy

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



class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user2 = User(
            email="test@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user2)
        db.session.commit()

        user3 = User(
            email="test3@test.com",
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        db.session.add(user3)
        db.session.commit()


        self.client = app.test_client()
        self.user2 = user2
        self.user3 = user3

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test5@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_follow(self):
        """Does basic follow work?"""


        follow = Follows(user_being_followed_id=self.user3.id, user_following_id=self.user2.id)

        db.session.add(follow)
        db.session.commit()

        added_follow = Follows.query.get((self.user3.id, self.user2.id))

        self.assertEqual(added_follow.user_being_followed_id ,self.user3.id)
        self.assertEqual(added_follow.user_following_id, self.user2.id)
        self.assertEqual(self.user3.followers[0].id, self.user2.id)
        self.assertEqual(self.user2.following[0].id, self.user3.id)

    def test_user_signup(self):
        """Does the signup classmethod work"""


        User.signup( 'Testusername', 'fakeemail@gmail.com', 'password', None)

        added_user = User.query.filter(User.username == 'Testusername').first()

        self.assertEqual(added_user.username, 'Testusername')

    def test_invalid_signup(self):
        """Do the signup requirements work"""

        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            User.signup( 'Testusername', 'test@test.com', 'password', None)
            db.session.commit()

    def test_authentication(self):
        """Does authenitcation work"""

        temp_user = User.signup( 'name', 'fakeemail2@gmail.com', 'password', None)
        db.session.commit()

        self.assertTrue(User.authenticate(temp_user.username, 'password'))
        self.assertFalse(User.authenticate(temp_user.username, 'djhfdjfhj'))
        self.assertFalse(User.authenticate('bad_user', 'password'))






