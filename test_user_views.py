from cgitb import html
from email import message
import os
from unittest import TestCase
from urllib import response
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from flask import redirect, url_for, request
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout

os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app, CURR_USER_KEY

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Test Case for User Views"""

    def setUp(self):
        """Create Test User"""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.register(
            username = "testytest",
            pwd = "yupp1234",
            email = "testytest@gmail.com",
            first_name = "testy",
            last_name = "test"
        )

        self.testuser_id = 1234
        self.testuser.id = self.testuser_id

        self.testworkout = Workout(
            title = "Test Title",
            description = "Test Description"
        )

        self.testworkout_id = 1234
        self.testworkout.id = self.testworkout_id

        db.session.commit()


    def tearDown(self):
        """Delete Test User Table"""
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_home_logged_out(self):
        """Test Home Page View Logged Out"""
        with self.client as c:
            res = c.get("/home")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Log in", html)
            self.assertIn("Create Account", html)
            self.assertNotIn("Create Workout", html)
            self.assertNotIn("Log out", html)


    def test_home_logged_in(self):
        """Test Home Page View Logged In"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get(f"/user/{self.testuser_id}")
            soup = BeautifulSoup(str(res.data), "html.parser")
            drpdwn_found = soup.find_all("li", class_="nav-item dropdown")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(drpdwn_found), 1)


    def test_register_view(self):
        """Test Register Page View"""
        with self.client as c:
            res = c.get("/register")
            soup = BeautifulSoup(str(res.data), "html.parser")
            register_form = soup.find_all("form", class_="register-form")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(register_form), 1)


    def test_register_user(self):
        """Test User Registration"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get("/register")
            
            self.assertEqual(resp.status_code, 302)


    def test_login_page_view(self):
        """Test Login Page View"""
        with self.client as c:
            res = c.get("/login")
            soup = BeautifulSoup(str(res.data), "html.parser")
            login_form = soup.find_all("form", class_="login-form")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(login_form), 1)


    def test_login_user(self):
        """Test User Login"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            res = c.get("/login")
            
            self.assertEqual(res.status_code, 302)


    def test_edit_user_logged_out(self):
        """Test Edit User Page View when not signed in"""
        with self.client as c:

            res = c.get(f"/user/{self.testuser_id}/edit")
            soup = BeautifulSoup(str(res.data), "html.parser")
            edit_form = soup.find_all("form", class_="edit-user-form")

            self.assertEqual(res.status_code, 302)
            self.assertNotEqual(len(edit_form), 1)


    def test_edit_user_logged_in(self):
        """Test Edit User Page View when signed in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            res = c.get(f"/user/{self.testuser_id}/edit")
            soup = BeautifulSoup(str(res.data), "html.parser")
            edit_form = soup.find_all("form", class_="edit-user-form")
            delete_user_form = soup.find_all("form", class_="delete-user-form")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(edit_form), 1)
            self.assertEqual(len(delete_user_form), 1)


    def test_delete_user_logged_out(self):
        """Test Deleting User When Not Signed In"""
        with self.client as c:
            res = c.get(f"/user/{self.testuser_id}/delete")
        
            self.assertEqual(res.status_code, 302)



    def test_delete_user_logged_in(self):
        """Test Deleting User When Signed In"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get(f"/user/{self.testuser_id}/delete")

            self.assertEqual(res.status_code, 302)


    def test_access_undefined_route(self):
        """Test Attempt to access an undefined route """
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                
            res = c.get("/user/this-page-doesnt-exist")

            self.assertEqual(res.status_code, 404)