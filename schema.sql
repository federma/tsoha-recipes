CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    instructions TEXT,
    created_at TIMESTAMP,
    user_id INTEGER REFERENCES users 
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT,
    amount INTEGER,
    unit TEXT,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    sent_at TIMESTAMP,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);