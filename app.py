from crypt import methods
import os
from click import edit 
from flask import Flask, render_template, request, redirect, jsonify, session, g, flash
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from requests import delete, post
from sqlalchemy import delete, func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from models import db, connect_db, DaysOfWeek, User, Workout, Exercise
from forms import LoginForm, RegisterForm, EditUserFrom, UpdatePwdForm, WorkoutInfoForm, AddExercToWorkoutForm, ExerciseSearchForm

CURR_USER_KEY = "curr_user"
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get("DATABASE_URL", "postgresql:///workout_planner"))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SECRET_KEY"] = "yupp1234"
toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

################################################################################################################################
### USER REGISTER/LOGIN/LOGOUT HANDlING ###
################################################################################################################################

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
def home():
    """Base redirects to login page if user is not logged in"""
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
            

        flash("Email or Password are incorrect.", 'danger')


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
        return redirect("/")

    # validate_email = User.query.filter_by(email=email).first()
    # validate_username = User.query.filter(username).first()

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            new_user = User.register(username, password, email, first_name, last_name)

            db.session.add(new_user)
            db.session.commit()
            
        except IntegrityError:
            db.session.rollback()
            if User.query.filter(User.email==form.email.data).first():
               flash("Email is unavailable.", "danger")
            if User.query.filter(User.username == form.username.data).first():
                flash("Username is unavailable.", "danger")
            return render_template('/user/register.html', form=form)
        
        session['username'] = new_user.username
        # Flash welcome, and redirect user to the secret page.
        if new_user:
            do_login(new_user)
            flash(f"Hello, {new_user.username}!", "success")
            return redirect("/")

    else:
        return render_template('/user/register.html', form=form)


################################################################################################################################
### USER ROUTE HANDlING ###
################################################################################################################################

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def user_home(user_id):
    """Returns Users home page, if user not logged in will redirect to login page."""
    if not g.user:
        return redirect("/")
    
    user = User.query.get_or_404(user_id)

    workout = (Workout.query.filter(Workout.user_id == user_id).all())


    return render_template("/user/user_home.html", user=user, workout=workout )


@app.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    """ Returns Edit User page, if user not logged in, will redirect to login page."""
    if not g.user:
        return redirect("/login")
    
    user = User.query.get_or_404(user_id)

    workout = (Workout.query.filter(Workout.user_id == user_id).all())

    form = EditUserFrom()
 
    if form.validate_on_submit():
        try:
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.username = form.username.data
            
            db.session.commit()
            return redirect(f"/user/{g.user.id}")

        except IntegrityError:
            db.session.rollback()
            if User.query.filter(form.username.data!=g.user.username).first():
                flash("Username is unavailable.", "danger")
            elif User.query.filter(form.email.data!=g.user.email).first():
                flash("Email is unavailable.", "danger")
            elif User.query.filter(form.username.data==g.user.username).first():
                return
            elif User.query.filter(form.email.data==g.user.email).first():
                return
            return redirect(f"/user/{g.user.id}/edit")

    elif request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.username.data = user.username



    return render_template("/user/edit_user.html", user=user, workout=workout, form=form)


@app.route('/user/<int:user_id>/password/change', methods=["GET", "POST"])
def update_password(user_id):
    """Form allowing user to chagne password. First confirming current password and then resetting password"""
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



@app.route('/user/<int:user_id>/delete', methods=["GET","POST"])
def delete_user(user_id):
    """Delete user."""

    if not g.user:
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    workout = (Workout.query.filter(Workout.user_id == user_id).all())

    do_logout()

    for workout in workout:
        if workout.user_id == user.id:
            db.session.delete(workout)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")




################################################################################################################################
### WORKOUT ROUTE HANDlING ###
################################################################################################################################

@app.route("/workout/<int:workout_id>")
def workout_show(workout_id):
    """Returns page of workout title and description if user has """

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
        specific days of week, and delete"""
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
    """Form allowing multiple exercises to be added to users workout."""
    if not g.user:
        return redirect("/")

    workout = Workout.query.get_or_404(workout_id)

    form = AddExercToWorkoutForm()

    if form.validate_on_submit():
        workout.day_1 = form.day_id_1.data
        workout.day_2 = form.day_id_2.data
        workout.day_3 = form.day_id_3.data
        workout.exercise_1 = form.exercise_id_1.data
        workout.exercise_2 = form.exercise_id_2.data
        workout.exercise_3 = form.exercise_id_3.data
        workout.exercise_4 = form.exercise_id_4.data
        workout.exercise_5 = form.exercise_id_5.data
        workout.exercise_6 = form.exercise_id_6.data
        workout.exercise_7 = form.exercise_id_7.data
        workout.exercise_8 = form.exercise_id_8.data
        workout.exercise_9 = form.exercise_id_9.data
        
        db.session.commit()
        return redirect(f"/user/{g.user.id}")
    
    elif request.method == "GET":
        form.day_id_1.data = DaysOfWeek.query.filter_by(id=workout.days_id_1).first()
        form.day_id_2.data = DaysOfWeek.query.filter_by(id=workout.days_id_2).first()
        form.day_id_3.data = DaysOfWeek.query.filter_by(id=workout.days_id_3).first()
        form.exercise_id_1.data = Exercise.query.filter_by(id=workout.exercise_id_1).first()
        form.exercise_id_2.data = Exercise.query.filter_by(id=workout.exercise_id_2).first()
        form.exercise_id_3.data = Exercise.query.filter_by(id=workout.exercise_id_3).first()
        form.exercise_id_4.data = Exercise.query.filter_by(id=workout.exercise_id_4).first()
        form.exercise_id_5.data = Exercise.query.filter_by(id=workout.exercise_id_5).first()
        form.exercise_id_6.data = Exercise.query.filter_by(id=workout.exercise_id_6).first()
        form.exercise_id_7.data = Exercise.query.filter_by(id=workout.exercise_id_7).first()
        form.exercise_id_8.data = Exercise.query.filter_by(id=workout.exercise_id_8).first()
        form.exercise_id_9.data = Exercise.query.filter_by(id=workout.exercise_id_9).first()
    

    return render_template("workout/manual_exerc_add.html", form=form, workout=workout)


@app.route("/workout/<int:workout_id>/delete", methods=["GET","POST"])
def delete_workout(workout_id):
    """Delete current workout"""
    if not g.user:
        return redirect("/")

    workout = Workout.query.get_or_404(workout_id)

    db.session.delete(workout)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")



################################################################################################################################
### EXERCISE ROUTE HANDlING ###
################################################################################################################################

@app.context_processor
def base():
    """Pass Data to NavBar"""
    form = ExerciseSearchForm()
    return dict(form=form)


@app.route("/search", methods=["POST"])
def exercise_search():
    form = ExerciseSearchForm()

    exerc = Exercise.query

    if form.validate_on_submit():
        # Get data from submitted form
        searched = form.searched.data

        # Query the Database
        exerc = exerc.filter(Exercise.name.ilike('%' + searched + '%'))
        exerc = exerc.order_by(Exercise.id).all()

        return render_template("exercise/exercise_search.html", form=form, searched=searched, exerc=exerc)

    return render_template("exercise/exercise_search.html")


@app.route("/exercise/<int:exercise_id>", methods=["GET"])
def exercise_show(exercise_id):

    exerc = Exercise.query.get_or_404(exercise_id)
    equip = Exercise.query.filter_by(equipment_id=exerc.equipment_id)


    return render_template("exercise/exercise_show.html", exerc=exerc, equip=equip)



################################################################################################################################
### ERROR ROUTE HANDlING ###
################################################################################################################################

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req