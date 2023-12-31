CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE learning_journeys (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    learning_journey_id INTEGER REFERENCES learning_journeys,
    sent_at TIMESTAMP
);
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    UNIQUE (name, user_id)
);
CREATE TABLE entry_tags (
    id SERIAL PRIMARY KEY,
    entry_id INT REFERENCES entries ON DELETE CASCADE,
    tag_id INT REFERENCES tags ON DELETE CASCADE
);
CREATE TABLE breakthroughs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    entry_id INTEGER REFERENCES entries ON DELETE CASCADE,
    UNIQUE (user_id, entry_id)
);