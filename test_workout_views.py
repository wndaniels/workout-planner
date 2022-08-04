import os, requests
from unittest import TestCase
from bs4 import BeautifulSoup
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout

os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app, CURR_USER_KEY
db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class WorkoutModelTestCase(TestCase):
    """Test Case for Workout Model"""

    def setUp(self):
        """Set Up Workout Model"""

        db.session.close()
        db.drop_all()
        db.create_all()

        #####
        # Seed Days of Week data from API into db
        #####
        days_data = requests.get("https://wger.de/api/v2/daysofweek/?format=json").json()
        days_of_week = [DaysOfWeek(days_of_week=days["day_of_week"]) for days in days_data["results"]]

        db.session.add_all(days_of_week)
        db.session.commit()

        self.days_1 = DaysOfWeek.query.filter_by(id=DaysOfWeek.id).first()

        #####
        # Seed Equipment data from API into db
        #####
        newEquipData = []
        equip_data = requests.get("https://wger.de/api/v2/equipment/?format=json").json()
        for equip in equip_data["results"]:
            newEquipData.append(Equipment(id=equip["id"], name=equip["name"]))

        db.session.add_all(newEquipData)
        db.session.commit()

        #####
        # Seed Excercise data from API into db
        #####
        newExercData = []
        exerc_data = requests.get("https://wger.de/api/v2/exercise/?format=json&limit=231&language=2").json()

        for exerc in exerc_data["results"]:
            equip_id = exerc["equipment"][0] if len(exerc["equipment"]) > 0 else 7
            descript = exerc["description"]
            soup = BeautifulSoup(descript, features='html.parser')

            newExercData.append(Exercise(name=exerc["name"], description=soup.get_text(), equipment_id=equip_id))

        db.session.add_all(newExercData)
        db.session.commit()

        self.exerc_1 = Exercise.query.filter_by(id=Exercise.id).first()

        self.u1_id = 1111
        u1 = User.register("testuser1", "testpassword", "testuser1email@gmail.com", "testy1", "test1")
        u1.id = self.u1_id
        db.session.commit()

        self.u2_id = 2222
        u2 = User.register("testuser2", "testpassword", "testuser2email@gmail.com", "testy2", "test2")
        u2.id = self.u2_id
        db.session.commit()

        self.u1 = User.query.get(self.u1_id)
        self.u2 = User.query.get(self.u2_id)
        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    

    def test_view_create_workout_form_logged_out(self):
        """Test View Creating Workout From When Not Signed In"""
        with self.client as c:
            res = c.get("/workout/create")
        
            self.assertEqual(res.status_code, 302)


    def test_view_create_workout_form_logged_in(self):
        """Test View Creating Workout From When Signed In"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            res = c.get("/workout/create")
            soup = BeautifulSoup(str(res.data), "html.parser")
            create_workout_form = soup.find_all("form", class_="create-workout-form")
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(create_workout_form), 1)


    def test_create_new_workout_logged_out(self):
        """Test Create New Workout When Not Signed In"""
        with self.client as c:
            res = c.post("/workout/create", data={"title": "Test Title", "description": "Test Description"})

            self.assertEqual(res.status_code, 302)
    

    def test_create_new_workout_unauthorized(self):
        """Test Create New Workout When Signed In"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 123456789
            

            res = c.post("/workout/create", data={"title": "Test Title", "description": "Test Description"})

            self.assertEqual(res.status_code, 302)


    def test_create_new_workout_logged_in(self):
        """Test Create New Workout When Signed In"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
            
            res = c.post("/workout/create", data={"title": "Test Title", "description": "Test Description"}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test Title", html)
            self.assertIn("Add/Edit Exercise List", html)