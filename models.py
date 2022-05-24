from enum import unique
from math import sqrt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey, null
from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()

def submit_data(model):
    """Add and commit model to database"""
    db.session.add(model)
    db.session.commit()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    first_name = db.Column(
        db.Text,
        nullable = False
    )

    last_name = db.Column(
        db.Text,
        nullable = False
    )

    email = db.Column(
        db.Text,
        unique = True,
        nullable = False
    )


    username = db.Column(
        db.String(30),
        unique = True,
        nullable = False
    )

    password = db.Column(
        db.Text,
        nullable = False 
    )

    def __repr__(self):
        return f"<User {self.id}>"
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        username = username
        hashed = bcrypt.generate_password_hash(pwd, rounds=12)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        submit_data(user)

        return user
    @classmethod
    def authenticate(cls, username, pwd):
        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
    
    @classmethod
    def check_username(cls, username) -> bool:
        return cls.query.filter_by(username=username).one_or_none()

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username
        }

class Workout(db.Model):
    """Workout Model"""

    __tablename__ = "workouts"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    title = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )

    user = db.relationship(
        "User",
        backref="workouts"
    )

    def __repr__(self):
        return f"<Workout {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description
        }

class DaysOfWeek(db.Model):
    """DaysOfWeek Model"""

    __tablename__ = "daysofweek"

    days_of_week = db.Column(
        db.Text,
        primary_key = True
    )

    def __repr__(self):
        return f"<DaysOfWeek {self.days_of_week}>"
    
    def serialize(self):
        return {
            "day": self.days_of_week
        }

class Equiment(db.Model):
    """Equipment Model"""
    
    __tablename__ = "equipment"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.Text,
        unique = True
    )

    def __repr__(self):
        return f"<Equipment {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Exercise(db.Model):
    """Exercise Model"""

    __tablename__ = "exercises"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.Text,
        unique = True
    )

    description = db.Column(
        db.Text
    )

    equipment_name = db.Column(
        db.Text,
        db.ForeignKey("equipment.name")
    )

    equipment = db.relationship(
        "Equipment", 
        backref="exercises"
    )

    def __repr__(self):
        return f"<Excercise excercise:{self.name} equipment:{self.equipment_name}>"
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "equipment_name": self.equipment_name
        }

class WorkoutPlan(db.Model):
    """WorkoutPlan Model"""

    __tablename__ = "workout_plan"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    workouts_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id")
    )

    day_of_week = db.Column(
        db.Text,
        db.ForeignKey("daysofweek.days_of_week")
    )

    equipment_name = db.Column(
        db.Text,
        db.ForeignKey("equipment.name")
    )

    exercise_name = db.Column(
        db.Text,
        db.ForeignKey("exercises.name")
    )

    equipment = db.relationship(
        "Equipment", 
        backref="workout_plan"
    )

    excercise = db.relationship(
        "Exercise",
        backref="workout_plan"
    )

    def __repr__(self):
        return f"<WorkoutPlan days:{self.day_of_week} exercise:{self.exercise_name} equipment:{self.equipment_name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "workouts_id": self.workouts_id,
            "day_of_week": self.day_of_week,
            "equipment": self.equipment_name,
            "exercise": self.exercise_name
        }