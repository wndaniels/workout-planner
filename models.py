from email.policy import default
from enum import unique
from math import sqrt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import ForeignKey, Unicode, null, func
from sqlalchemy.dialects import postgresql
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

###########################################################################################
### USER MODEL ###
###########################################################################################

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
        nullable = True
    )

    last_name = db.Column(
        db.Text,
        nullable = True
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

        if username is not None:
            username = username.lower()


        if email is not None:
            email = email.lower()
        

            
        hashed = bcrypt.generate_password_hash(pwd, rounds=12)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        submit_data(user)

        return user


    @classmethod
    def authenticate(cls, username, pwd):
        user = cls.query.filter_by(username=username.lower()).one_or_none()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


###########################################################################################
### DAYS OF WEEK MODEL ###
###########################################################################################

class DaysOfWeek(db.Model):
    """DaysOfWeek Model"""

    __tablename__ = "daysofweek"

    id = db.Column(
        db.Integer, 
        primary_key = True
    )

    days_of_week = db.Column(
        db.Text,
        unique=True
    )

    def __repr__(self):
        return f"<DaysOfWeek {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "days_of_week": self.days_of_week
        }
    
def days_query():
        return DaysOfWeek.query


###########################################################################################
### EQUIPMENT MODEL ###
###########################################################################################
    
class Equipment(db.Model):
    """Equipment Model"""
    
    __tablename__ = "equipment"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    name = db.Column(
        db.Text
    )

    def __repr__(self):
        return f"<Equipment {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


###########################################################################################
### EXERCISE MODEL ###
###########################################################################################

class Exercise(db.Model):
    """Exercise Model"""

    __tablename__ = "exercises"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )

    equipment_id = db.Column(
        db.Integer,
        db.ForeignKey("equipment.id")
    )

    equip_id = db.relationship(
        "Equipment",
        backref="exercises"
    )


    def __repr__(self):
        return f"<Excercise {self.id} >"
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "equipment_id": self.equipment_id
        }

def excer_query():
        return Exercise.query


###########################################################################################
### WORKOUT MODEL ###
###########################################################################################

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
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable = False
    )

    title = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )

    days_id_1 = db.Column(
        db.Integer,
        db.ForeignKey("daysofweek.id", ondelete="cascade")
    )

    days_id_2 = db.Column(
        db.Integer,
        db.ForeignKey("daysofweek.id", ondelete="cascade")
    )

    days_id_3 = db.Column(
        db.Integer,
        db.ForeignKey("daysofweek.id", ondelete="cascade")
    )

    exercise_id_1 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_2 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_3 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_4 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_5 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_6 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_7 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_8 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    exercise_id_9 = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="cascade")
    )

    user = db.relationship(
        "User",
        backref="workouts"
    )

    day_1 = db.relationship(
        "DaysOfWeek",
        foreign_keys=[days_id_1]
    )

    day_2 = db.relationship(
        "DaysOfWeek",
        foreign_keys=[days_id_2]
    )

    day_3 = db.relationship(
        "DaysOfWeek",
        foreign_keys=[days_id_3]
    )

    exercise_1 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_1]
    )

    exercise_2 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_2]
    )

    exercise_3 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_3]
    )

    exercise_4 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_4]
    )

    exercise_5 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_5]
    )

    exercise_6 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_6]
    )

    exercise_7 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_7]
    )

    exercise_8 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_8]
    )

    exercise_9 = db.relationship(
        "Exercise",
        foreign_keys=[exercise_id_9]
    )
    
    def __repr__(self):
        return f"<Workout {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "day_id_1": self.days_id_1,
            "day_id_2": self.days_id_2,
            "day_id_3": self.days_id_3,
            "exercise_id_1": self.exercise_id_1,
            "exercise_id_2": self.exercise_id_2,
            "exercise_id_3": self.exercise_id_3,
            "exercise_id_4": self.exercise_id_4,
            "exercise_id_5": self.exercise_id_5,
            "exercise_id_6": self.exercise_id_6,
            "exercise_id_7": self.exercise_id_7,
            "exercise_id_8": self.exercise_id_8,
            "exercise_id_9": self.exercise_id_9
        }

    # @classmethod
    # def create_workout(cls, title, description):

    #     workout = cls(title=title, description=description)
    #     submit_data(workout)

    #     return workout
