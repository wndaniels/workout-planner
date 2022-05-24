from crypt import methods
import os 
from flask import Flask, render_template, request, redirect, jsonify, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from models import db, connect_db, User, Workout, Exercise
from forms import LoginForm, Register

TOKEN = "curr_user"
app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///workout_planner")

# API_BASE_URL = "https://wger.de/api/v2/"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL if DATABASE_URL in ["postgresql:///workout_planner_test", "postgresql:///workout_planner"] else DATABASE_URL.replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


connect_db(app)

app.config["SECRET_KEY"] = "s3cr1t059"

debug = DebugToolbarExtension(app)

####
### USER ROUTE HANDlING ###
####
@app.before_request
def add_user_to_g():
    """Add user to flask's global g variable"""

    if TOKEN in session:
        g.user = User.query.get(session[TOKEN])
    
    else:
        g.user = None

@app.route("/", methods=["GET", "POST"])
def home():
    """Returns redirect to login page"""

    return redirect("/login")

@app.route("/login", methods=["GET"])
def login():
    """User Login Routee"""

    if TOKEN in session:
        return redirect("/workouts")
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/workouts")
        else:
            form.username.errors = ['Invalide Username and/or Password']
            form.password.errors = ['Invalide Username and/or Password']

    return render_template('/user/login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if 'username' in session:
        return redirect('/users/{username}')

    form = Register()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append(
                "Username is not available, please pick another.")
            return render_template('/user/register.html', form=form)
        
        session['username'] = new_user.username
        # Flash welcome, and redirect user to the secret page.
        flash(f"Welcome {new_user.username}, your account has been created")
        return redirect(f'/users/{username}')
    else:
        return render_template('/user/register.html', form=form)
    

 ####
### WORKOUT ROUTE HANDlING ###
####

@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    return render_template("/workout/workouts")


####
### ERROR ROUTE HANDlING ###
####
# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Renders error page if URL not found, or if there is a server error."""

#     if isinstance(e, HTTPException):
#         return render_template("error.html", error=e, title="Something went wrong.")
#     else:
#         return render_template("error.html", error=e, title="Something went wrong."), 500