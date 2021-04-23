CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    created_at TIMESTAMP
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    instructions TEXT,
    portions INTEGER,
    created_at TIMESTAMP,
    user_id INTEGER REFERENCES users,
    views INTEGER,
    visible INTEGER
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
    user_id INTEGER REFERENCES users,
    visible INTEGER
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    created_at TIMESTAMP
);

CREATE TABLE shopping_list (
    id SERIAL PRIMARY KEY,
    -- cart_id is reserved for future use, could be used for saving multiple shopping-lists for later use
    -- or also saving favourites (f.e. items with cart_id 1 could be favourites). Not yet implemented in the code.
    cart_id INTEGER,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    inserted_at TIMESTAMP
)