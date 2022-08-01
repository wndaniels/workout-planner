import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout


os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test case for User model class"""


    def setUp(self):
        """Create test client and sample data"""
        
        db.session.close()
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


###########################################################################################
### TEST REGISTRAION CLASSMETHOD ###
###########################################################################################

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
        """ Test for invalidity of username """ 
        try: 
            invalid_username = User.register(None, "password", "test@gmail.com", "Test", "Tester")
            u_id = 12345
            invalid_username.id = u_id
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            

    def test_unavailable_username_registration(self):
        """ Test for availability of username """
        try: 
            invalid_username = User.register("frankyfrank", "password", "test@gmail.com", "Test", "Tester")
            u_id = 2468
            invalid_username.id = u_id
            db.session.commit()
        except IntegrityError:
            return
            db.session.rollback()


###########################################################################################
### TEST AUTHENTICATION CLASSMETHOD ###
###########################################################################################

    def test_user_authenticate(self):
        """Test User classmethod AUTHENTICATE """

        user1 = User.authenticate(self.u1.username, "yupp1234")
        self.assertIsNotNone(user1)
        self.assertEqual(user1.id, self.u1_id)

        user2 = User.authenticate(self.u2.username, "yupp1234")
        self.assertIsNotNone(user2)
        self.assertEqual(user2.id, self.u2_id)

        self.assertNotEqual(user1.id, self.u2_id)
    
    def test_username_case_insensitive(self):
        self.assertTrue(User.authenticate("frankyfrank", "yupp1234"))
        self.assertTrue(User.authenticate("fRaNkYfRaNk", "yupp1234"))
        self.assertTrue(User.authenticate("billybill", "yupp1234"))
        self.assertTrue(User.authenticate("bIlLyBiLl", "yupp1234"))

    def test_incorrect_password(self):
        self.assertFalse(User.authenticate("frankyfrank", "yupp123456789"))
        self.assertFalse(User.authenticate("billybill", "yupp34"))
    

