from crypt import methods
import os
from click import edit 
from flask import Flask, render_template, request, redirect, jsonify, session, g, flash
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash
from models import DaysOfWeek, Equipment, db, connect_db, User, Workout, Exercise
from forms import LoginForm, RegisterForm, EditUserFrom, UpdatePwdForm, WorkoutInfoForm, AddExercToWorkoutForm

CURR_USER_KEY = "curr_user"
app = Flask(__name__)
bcrypt = Bcrypt(app)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///workout_planner")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL if DATABASE_URL in ["postgresql:///workout_planner_test", "postgresql:///workout_planner"] else DATABASE_URL.replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


connect_db(app)

app.config["SECRET_KEY"] = "yupp1234"

# debug = DebugToolbarExtension(app)

####
### USER ROUTE HANDlING ###
####
@app.before_request
def add_user_to_g():
    """Add user to flask's global g variable"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None



def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id



def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route("/", methods=["GET", "POST"])
def base():
    """Base redirects to home page"""

    return redirect("/home")



@app.route("/home", methods=["GET", "POST"])
def home():
    """ Returns home page, if user logged in will redirect to users home page """
    if g.user:
        return redirect(f"/user/{g.user.id}")
    
    """ MAYBE PUT A TIMED MODAL THAT SHOWS UP FOR USER TO LOGIN """

    return redirect("/login")



@app.route("/login", methods=["GET", "POST"])
def login():
    """User Login Route, if user logged in, redirect to user home. """

    if g.user:
        return redirect("/")
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('user/login.html', form=form)



@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    return redirect('/')



@app.route("/register", methods=["GET", "POST"])
def register():
    """Returns register user page, if user logged in, log out and continue to register page. """

    if g.user:
        do_logout()
        """ MAYBE PUT MODAL IN THAT SHOWS IF SOMEONE IS WANTING TO ACCESS REGISTER PAGE WHILE SIGNED IN """

    form = RegisterForm()

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
        return redirect('/login')
    else:
        return render_template('/user/register.html', form=form)



@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def user_home(user_id):
    """Returns Users home page, if user not logged in will redirect to login page."""
    if not g.user:
        return redirect("/")
    
    user = User.query.get_or_404(user_id)

    workout = (Workout
                .query
                .all())


    return render_template("/user/user_home.html", user=user, workout=workout )


@app.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """ Returns Edit User page, if user not logged in, will redirect to login page."""
    if not g.user:
        return redirect("/login")
    
    user = User.query.get_or_404(user_id)

    form = EditUserFrom()


    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.username = form.username.data
        
        db.session.commit()
        return redirect(f"/user/{g.user.id}")
    
    elif request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.username.data = user.username

    return render_template("/user/edit_user.html", user=user, form=form)


@app.route('/user/<int:user_id>/password/change', methods=["GET", "POST"])
def update_password(user_id):
    if not g.user:
        return redirect("/login")
    
    user = User.query.get_or_404(user_id)

    form = UpdatePwdForm()

    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.new_pwd.data).decode("utf-8")
        db.session.commit()
        flash("Password has been updated", 'success')
        return redirect(f"/user/{g.user.id}")

    return render_template("/user/update_pwd.html", user=user, form=form)



@app.route('/user/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/login")



####
### WORKOUT ROUTE HANDlING ###
####
@app.route("/workout/<int:workout_id>", methods=["GET","POST"])
def workout_show(workout_id):

    if not g.user:
        return redirect("/")
    
    workout = Workout.query.get_or_404(workout_id)
    return render_template("workout/workout_list.html", workout=workout)



@app.route("/workout/create", methods=["GET", "POST"])
def create_workout():
    """Returns Create Workout page, if User not logged in, redirects to login page"""
 
    if not g.user:
        return redirect("/login")
    
    if g.user.workouts:
        return redirect(f"/user/{g.user.id}")
    
    form = WorkoutInfoForm()

    if form.validate_on_submit():
        new_workout = Workout(user_id=g.user.id, title=form.title.data, description=form.description.data) 
        g.user.workouts.append(new_workout)
        db.session.commit()
        return redirect(f"/user/{g.user.id}")

    return render_template("workout/create_workout.html", form=form)
    



@app.route("/workout/<int:workout_id>/edit", methods=["GET", "POST"])
def edit_workout(workout_id):
    """Allows user to edit their workout title and description, as well as add workouts to 
        specific days of week, and delete """
    if not g.user:
        return redirect("/")

    workout = Workout.query.get_or_404(workout_id)
    
    form = WorkoutInfoForm(obj=workout)

    if form.validate_on_submit():
        workout.title = form.title.data
        workout.description = form.description.data
        
        db.session.commit()
        return redirect(f"/user/{g.user.id}")
    
    elif request.method == "GET":
        form.title.data = workout.title
        form.description.data = workout.description

    
    return render_template("workout/edit_workout.html", form=form, workout=workout)


@app.route("/workout/<int:workout_id>/add-exercise", methods=["GET", "POST"])
def add_exercise(workout_id):
    if not g.user:
        return redirect("/")

    workout = Workout.query.get_or_404(workout_id)

    form = AddExercToWorkoutForm()

    if form.validate_on_submit():
        equip = Equipment.query.get_or_404(form.exercise_id.data.equipment_id)
        workout.days = form.day_of_week.data
        workout.exercise = form.exercise_id.data or workout.exercise_id.name
        workout.equipment_id = equip.id
        
        db.session.commit()
        return redirect(f"/user/{g.user.id}")
    
    elif request.method == "GET":
        form.day_of_week.data = DaysOfWeek.query.filter_by(id=workout.days_id).first()
        form.exercise_id.data = Exercise.query.filter_by(id=workout.exercise_id).first()

    return render_template("workout/manual_exerc_add.html", form=form, workout=workout)

    


@app.route("/workout/<int:workout_id>/delete", methods=["GET","POST"])
def delete_workout(workout_id):

    if not g.user:
        return redirect("/")

    workout = Workout.query.get_or_404(workout_id)

    db.session.delete(workout)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")



####
### EXERCISE ROUTE HANDlING ###
####

@app.route("/exercise/<int:exercise_id>", methods=["GET"])
def exercise_show(exercise_id):

    exerc = Exercise.query.get_or_404(exercise_id)

    return render_template("exercise/exercise_show.html", exerc=exerc)



####
### ERROR ROUTE HANDlING ###
####

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Renders error page if URL not found, or if there is a server error."""

    if isinstance(e, HTTPException):
        return render_template("error.html", error=e, title="Something went wrong.")
    else:
        return render_template("error.html", error=e, title="Something went wrong."), 500