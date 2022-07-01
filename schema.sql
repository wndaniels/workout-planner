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
    last_name TEXT NOT NULL,
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
    days_id INTEGER REFERENCES daysofweek,
    equipment_id INTEGER REFERENCES equipment,
    exercise_id INTEGER REFERENCES exercises
);

