# WELCOME TO WORKOUT PLANNER
- API: https://wger.de/en/software/api
- DEPLOYED APP: 

## Description:
Workout Planner is a web application that containing hundreds of exercise routines. Users will be able to create an account, 
search through the vast list of available exercises, and create a three day workout program containing the exercises per day. 
The current version of the application is proof of concept and has the ability to be heavily built upon. 

## Features:
- Anon users and accoutn holders alike are able to filter exercises via keywords in name via search bar.
- User accounts
  - Login and registration handled on serverside with use of Flask and WTForms.

## Getting Start:
- Firstly, clone the Workout Planner repository.
- Once all files are downloaded, create a virtual environment. `python3 -m venv venv`
- Install PostgreSQL. `https://www.postgresql.org/download/`
- Install all required dependencies `pip install requirments.txt`
- Create db and schema `psql < schema.sql`
- Seed db from API `python seed.py`
- Start Flask server `flask run`


## Tech Stack
### Languages:
- HTML5
- CSS
- Python
- PostgreSQL

### Libraries/Tools:
- Bcrypt
- Flask
- Flask-DebugToolbar
- Jinja2
- SQLAlchemy
- Unittest
- WTForms