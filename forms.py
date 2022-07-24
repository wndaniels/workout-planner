from curses.ascii import EM
from email import message
from email.policy import default
from lib2to3.pgen2.token import OP
from secrets import choice
from tokenize import String
from typing import Text
from flask_wtf import FlaskForm
from flask_login import current_user, login_manager
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SubmitField
from wtforms_alchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Optional, EqualTo, DataRequired, Email, ValidationError, Length
from models import days_query, excer_query, User


################################################################################################################################
### CUSTOMER FORM VALIDATION ###
################################################################################################################################

def validate_firstName(form, field):
    if not field.raw_data or not field.raw_data[0]: # Validate firt name has been entered
        raise ValidationError('First name is required')

def validate_email(form, field):
    if not field.raw_data or not field.raw_data[0]: # Validate email has been entered
        raise ValidationError('Valid email is required')
    if User.query.filter(User.email==field.data).first(): # Validate email entered is unused and available
        raise ValidationError('Email is unavailable')
            
def validate_username(form, field):
    if not field.raw_data or not field.raw_data[0]: # Validate username has been entered
        raise ValidationError('Username is required')
    if User.query.filter(User.username == field.data).first(): # Validate username entered is unused and available
        raise ValidationError('Username is unavailable')

def validate_password (form, field):
    if not field.raw_data or not field.raw_data[0]: # Validate password has been entered
        raise ValidationError('Password is required')

   
################################################################################################################################
### Forms ###
################################################################################################################################

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
        "First Name *",
        validators=[validate_firstName]
    )

    last_name = StringField(
        "Last Name", 
        validators=[Optional()]
    )

    email = EmailField(
        "Email *", 
        validators=[validate_email]
    )

    username = StringField(
        "Username *", 
        validators=[validate_username]
    )

    password = PasswordField(
        "Password *", 
        validators=[validate_password, EqualTo("confirm_password", message="Passwords must match")]
    )

    confirm_password = PasswordField(
        "Confirm Password *",
        # validators=[validate_password]
    )


class EditUserFrom(FlaskForm):
    """Edit User Information"""
    
    first_name = StringField(
        "First Name *",
        validators=[validate_firstName]
    )

    last_name = StringField(
        "Last Name", 
        validators=[Optional()]
    )

    email = EmailField(
        "Email *", 
        validators=[InputRequired()]
    )

    username = StringField(
        "Username *", 
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


class WorkoutInfoForm(FlaskForm):
    """Create Workout Template"""

    title = StringField(
        "Title", 
        validators=[InputRequired()]
    )

    description = TextAreaField(
        "Description", 
        validators=[Optional()]
    )


class AddExercToWorkoutForm(FlaskForm):
    """Add Workout Form"""
    
    day_id_1 = QuerySelectField(
        "Day of Week:", 
        query_factory=days_query,
        blank_text="Select a day of the week...",
        allow_blank=True,
        get_label='days_of_week',
        validators=[InputRequired()]
    )

    exercise_id_1 = QuerySelectField(
        "Exercise 1:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    exercise_id_2 = QuerySelectField(
        "Exercise 2:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    exercise_id_3 = QuerySelectField(
        "Exercise 3:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    day_id_2 = QuerySelectField(
        "Day of Week:", 
        query_factory=days_query,
        blank_text="Select a day of the week...",
        allow_blank=True,
        get_label='days_of_week',
        validators=[InputRequired()]
    )

    exercise_id_4 = QuerySelectField(
        "Exercise 4:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    exercise_id_5 = QuerySelectField(
        "Exercise 5:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    exercise_id_6 = QuerySelectField(
        "Exercise 6:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    day_id_3 = QuerySelectField(
        "Day of Week:", 
        query_factory=days_query,
        blank_text="Select a day of the week...",
        allow_blank=True,
        get_label='days_of_week',
        validators=[InputRequired()]
    )

    exercise_id_7 = QuerySelectField(
        "Exercise 7:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    exercise_id_8 = QuerySelectField(
        "Exercise 8:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )

    exercise_id_9 = QuerySelectField(
        "Exercise 9:",
        query_factory=excer_query,
        blank_text="Select an exercise...",
        allow_blank=True,
        get_label='name',
        validators=[InputRequired()]
    )


class ExerciseSearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")