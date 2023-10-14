CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE learning_journeys (
    id SERIAL PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    learning_journey_id INTEGER REFERENCES learning_journeys,
    sent_at TIMESTAMP
);