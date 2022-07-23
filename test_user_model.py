import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout


os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app


db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test case for User model class"""

    def setUp(self) -> None:
        """Create test client and sample data"""

        db.session.commit()

        self.testuser = User.register("frankyfrank", "yupp1234", "frankyfrank@gmail.com", "franky", "frank")
    
    def tearDown(self) -> None:
        """Empty users table"""
        
        User.query.delete()
    
    def test_user_register(self):
        """Test User classmethod REGISTER."""

        self.assertEqual(self.testuser.username, "frankyfrank")
        self.assertEqual(self.testuser.email, "frankyfrank@gmail.com")
        self.assertEqual(len(User.query.all()), 1)

    def test_user_authenticate(self):
        """Test User classmethod AUTHENTICATE """

        self.assertTrue(User.authenticate("frankyfrank", "yupp1234"))
        self.assertTrue(User.authenticate("fRaNkYfRaNk", "yupp1234"))
        self.assertFalse(User.authenticate("frankyfrankyyy", "yupp1234"))
        self.assertFalse(User.authenticate("frankyfrankyyy", "yupp34"))
    
    def test_user_check_username(self):
        """Test User classmethod CHECK_USERNAME"""

        self.assertTrue(User.check_username("frankyfrank"))
        self.assertTrue(User.check_username("fRaNkYfRaNk"))
        self.assertFalse(User.check_username("frankyfrankyyy"))