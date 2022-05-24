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

CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users,
    title TEXT,
    description TEXT 
);

CREATE TABLE daysofweek (
    days_of_week TEXT PRIMARY KEY
);

CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT, 
    equipment_name TEXT REFERENCES equipment
);

CREATE TABLE workout_plan (
    id SERIAL PRIMARY KEY,
    workout_id INTEGER REFERENCES workouts,
    day_of_week TEXT REFERENCES daysofweek,
    equipment_name TEXT REFERENCES equipment,
    exercise_name TEXT REFERENCES exercises
);