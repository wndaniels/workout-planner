DROP DATABASE IF EXISTS workout_planner;
CREATE DATABASE workout_planner;

\c workout_planner

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS workouts;
DROP TABLE IF EXISTS daysofweek;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS workout_plan;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE daysofweek (
    id INTEGER PRIMARY KEY,
    days_of_week TEXT UNIQUE
);

CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT, 
    equipment_id INTEGER REFERENCES equipment
);


CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users,
    title TEXT,
    description TEXT,
    days_id_1 INTEGER REFERENCES daysofweek,
    days_id_2 INTEGER REFERENCES daysofweek,
    days_id_3 INTEGER REFERENCES daysofweek,
    exercise_id_1 INTEGER REFERENCES exercises,
    exercise_id_2 INTEGER REFERENCES exercises,
    exercise_id_3 INTEGER REFERENCES exercises,
    exercise_id_4 INTEGER REFERENCES exercises,
    exercise_id_5 INTEGER REFERENCES exercises,
    exercise_id_6 INTEGER REFERENCES exercises,
    exercise_id_7 INTEGER REFERENCES exercises,
    exercise_id_8 INTEGER REFERENCES exercises,
    exercise_id_9 INTEGER REFERENCES exercises
);

