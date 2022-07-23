import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, DaysOfWeek, Equipment, Exercise, Workout


os.environ['DATABASE_URL'] = "postgresql:///workout_planner_test"
from app import app
db.create_all()



