from secrets import choice
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import InputRequired, Optional, EqualTo

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField(
        "Username", 
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password", 
        validators=[InputRequired()]
    )

class Register(FlaskForm):
    """Register User Form"""

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name", 
        validators=[InputRequired()]
    )

    email = EmailField(
        "Email", 
        validators=[InputRequired()]
    )

    username = StringField(
        "Username", 
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password", 
        validators=[InputRequired()]
    )

    confirm_password = PasswordField(
        "Confirm Password", 
        validators=[InputRequired(), EqualTo("password")]
    )

class CreateWorkout(FlaskForm):
    """Create Workout Template"""

    title = StringField(
        "Title", 
        validators=[Optional()]
    )

    description = StringField(
        "Description", 
        validators=[Optional()]
    )

class AddExercise(FlaskForm):
    """Add Exercise and Choose Days"""
    day_of_week = SelectField(
        "Day", 
        choice=[(0, "-")],
        validators=[InputRequired()]
    )

    exercise_name = SelectField(
        "Exercise",
        choice=[(0, "-")],
        validators=[InputRequired()]
    )
