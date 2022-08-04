import os, requests
from turtle import title
from unittest import TestCase
from sqlalchemy import exc
from bs4 import BeautifulSoup
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout


os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app



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

        self.u_id = 1111
        u = User.register("testuser", "testpassword", "testuseremail@gmail.com", "testy", "test")
        u.id = self.u_id
        db.session.commit()

        self.u = User.query.get(self.u_id)
        self.client = app.test_client()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    

    def test_workout_model(self):
        w = Workout(
            title="Test Title",
            description="Test Description",
            user_id=self.u_id,
            days_id_1=self.days_1.id,
            exercise_id_1=self.exerc_1.id
        )

        db.session.add(w)
        db.session.commit()

        self.assertEqual(self.days_1.days_of_week, "Monday")
        self.assertEqual(self.exerc_1.name, "2 Handed Kettlebell Swing")
        self.assertEqual(self.exerc_1.equipment_id, 10)
        self.assertNotEqual(self.days_1.days_of_week, "Tuesday")
        self.assertNotEqual(self.exerc_1.name, "Arnold Shoulder Press")