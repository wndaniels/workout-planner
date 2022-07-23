import os
from unittest import TestCase
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout

os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app, CURR_USER_KEY
db.create_all()
app.config['WTF_CSRF_ENABLED'] = False