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

    def setUp(self):
        """Create test client and sample data"""

        db.drop_all()
        db.create_all()

        u1 = User.register("frankyfrank", "yupp1234", "frankyfrank@gmail.com", "franky", "frank")
        u1_id = 1111
        u1.id = u1_id

        u2 = User.register("billybill", "yupp1234", "billybill@gmail.com", "billy", "bill")
        u2_id = 2222
        u2.id = u2_id

        db.session.commit()

        u1 = User.query.get(u1_id)
        u2 = User.query.get(u2_id)

        self.u1  = u1
        self.u1_id = u1_id

        self.u2  = u2
        self.u2_id = u2_id

        self.client = app.test_client()

    
    def tearDown(self):
        """Empty users table"""
        res = super().tearDown()
        db.session.rollback()
        return res
    

    def test_user_model(self):
        u = User(
            first_name = "george",
            last_name = None,
            email = "george@gmail.com",
            username = "georgio",
            password = "yupp1234"
        )

        db.session.add(u)
        db.session.commit()


################################################################################################################################
### TEST REGISTRAION CLASSMETHOD ###
################################################################################################################################

    def test_user_register(self):
        """Test User classmethod REGISTER."""

        u3 = User.register(
            "bobbybob",
            "yupp1234",
            "bobbybob@gmail.com",
            "bobby",
            "bob"
        )

        self.assertEqual(u3.username, "bobbybob")
        self.assertEqual(u3.email, "bobbybob@gmail.com")
        self.assertEqual(len(User.query.all()), 3)


        u4 = User.register(
            "peterpete",
            "yupp1234",
            "peter@gmail.com",
            "peter",
            "pete"
        )

        self.assertEqual(u4.username, "peterpete")
        self.assertEqual(u4.email, "peter@gmail.com")
        self.assertEqual(len(User.query.all()), 4)
    

    def test_invalid_username_registration(self):
        """Test for invalidity of username """ 

        username=None

        invalid_username = User.register(username, "test@gmail.com", "yupp1234", "Test", "Tester")
        uid = 12345
        invalid_username.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    # def test_user_authenticate(self):
    #     """Test User classmethod AUTHENTICATE """

    #     self.assertTrue(User.authenticate("frankyfrank", "yupp1234"))
    #     self.assertTrue(User.authenticate("fRaNkYfRaNk", "yupp1234"))
    #     self.assertFalse(User.authenticate("frankyfrankyyy", "yupp1234"))
    #     self.assertFalse(User.authenticate("frankyfrankyyy", "yupp34"))
    

    # def test_user_check_username(self):
    #     """Test User classmethod CHECK_USERNAME"""

    #     self.assertTrue(User.check_username("frankyfrank"))
    #     self.assertTrue(User.check_username("fRaNkYfRaNk"))
    #     self.assertFalse(User.check_username("frankyfrankyyy"))

