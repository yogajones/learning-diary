CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE learning_journeys (
    id SERIAL PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    learning_journey_id INTEGER REFERENCES learning_journeys,
    sent_at TIMESTAMP
);