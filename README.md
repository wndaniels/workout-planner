![alt text](img/headerimg.png)

# WELCOME TO WORKOUT PLANNER
- API: https://wger.de/en/software/api
- DEPLOYED APP: https://the-workout-planner.herokuapp.com
  - Test User: tester
  - Test Password: passer123

## Description:
Workout Planner is a web application that containing hundreds of exercise routines. Users will be able to create an account, 
search through the vast list of available exercises, and create a three day workout program containing three exercises per day. 
The current version of the application is proof of concept and has the ability to be heavily built upon. 

## Features:
- Anonymous users and account holders alike are able to filter exercises via keywords via search bar.
- User accounts
  - Login and registration handled on serverside with use of Flask and WTForms.

## Getting Start:
- Firstly, ensure correct version of Python is installed. `python-3.9.10 or later`
- Clone the Workout Planner repository. 
- Once all files are downloaded, create a virtual environment. `python3 -m venv venv`
- Install PostgreSQL. [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
- Install all required dependencies `pip install requirments.txt`
- Create db and schema `psql < schema.sql`
- Seed db from API `python seed.py`
- Start Flask server `flask run`


## Tech Stack
### Languages:
- CSS
- HTML5
- Flask
- Python
- PostgreSQL

### Libraries/Tools:
- Bcrypt - [https://pypi.org/project/bcrypt/](https://pypi.org/project/bcrypt/)
- Beautiful Soup - [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- Bootstrap - [https://getbootstrap.com/docs/5.2/getting-started/introduction/](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
- Flask - [https://flask.palletsprojects.com/en/2.1.x/](https://flask.palletsprojects.com/en/2.1.x/)
- Flask-DebugToolbar - [https://flask-debugtoolbar.readthedocs.io/en/latest/](https://flask-debugtoolbar.readthedocs.io/en/latest/)
- Jinja2 - [https://jinja.palletsprojects.com/en/3.1.x/](https://jinja.palletsprojects.com/en/3.1.x/)
- SQLAlchemy - [https://docs.sqlalchemy.org/en/14/](https://docs.sqlalchemy.org/en/14/)
- Unittest - [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)
- WTForms - [https://wtforms.readthedocs.io/en/3.0.x/](https://wtforms.readthedocs.io/en/3.0.x/)
