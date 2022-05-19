DROP DATABASE IF EXISTS workout_planner;
CREATE DATABASE workout_planner; 

\c workout_planner

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS workout;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS daysofweek;
DROP TABLE IF EXISTS workout_plan;

CREATE TABLE users (
    username text PRIMARY KEY,
    password text NOT NULL,
    email text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    image_url text
);

CREATE TABLE workout (
    id integer PRIMARY KEY,
    username text NOT NULL REFERENCES users,
    title text,
    description text
);

CREATE TABLE exercise (
    id integer PRIMARY KEY,
    name text,
    description text, 
    equipment integer
);

CREATE TABLE daysofweek (
    days_of_week text PRIMARY KEY
);

CREATE TABLE workout_plan (
    id integer PRIMARY KEY,
    workout_id integer NOT NULL REFERENCES workout,
    day_of_week text NOT NULL REFERENCES daysofweek,
    exercise_id integer NOT NULL REFERENCES exercise
);