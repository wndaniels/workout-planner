from email import message
from email.policy import default
from secrets import choice
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField, SearchField, HiddenField
from wtforms_alchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import InputRequired, Optional, EqualTo
from models import days_query, excer_query


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

class RegisterForm(FlaskForm):
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
        validators=[InputRequired(), EqualTo("confirm_password", message="Passwords must match")]
    )

    confirm_password = PasswordField(
        "Confirm Password"
    )

class EditUserFrom(FlaskForm):
    """Edit User Information"""
    
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

class UpdatePwdForm(FlaskForm):
    """Update Password"""
    current_pwd = PasswordField(
        "Current Password",
        validators=[InputRequired()]
    )

    new_pwd = PasswordField(
        "New Password", 
        validators=[InputRequired(), EqualTo("confirm_new_pwd", message="Passwords must match")]
    )

    confirm_new_pwd = PasswordField(
        "Confirm New Password",
        validators=[InputRequired()]
    )

class CreateWorkoutForm(FlaskForm):
    """Create Workout Template"""

    title = StringField(
        "Title", 
        validators=[InputRequired()]
    )

    description = TextAreaField(
        "Description", 
        validators=[Optional()]
    )


class EditWorkoutForm(FlaskForm):
    """Add Exercise and Choose Days"""
    title = StringField(
        "Title", 
        validators=[InputRequired()]
    )

    description = TextAreaField(
        "Description", 
        validators=[Optional()]
    )


    day_of_week = QuerySelectField(
        "Day of Week", 
        query_factory=days_query,
        blank_text="Select a day of the week...",
        allow_blank=True,
        get_label='days_of_week',
        validators=[InputRequired()]
    )

    exercise_id = QuerySelectField(
        "Exercise",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

   