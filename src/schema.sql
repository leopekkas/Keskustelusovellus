CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER
);

CREATE TABLE message_areas (
    id SERIAL PRIMARY KEY,
    name text,
    user_id INTEGER REFERENCES users
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    owner_id INTEGER REFERENCES users,
    message_area_id INTEGER REFERENCES message_areas,
    created_at TIMESTAMP
);

CREATE TABLE access_rights (
    message_area_id INTEGER REFERENCES message_areas, user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    topic_id INTEGER REFERENCES topics,
    sent_at TIMESTAMP,
    visibility INTEGER
);

INSERT INTO message_areas (id, name) VALUES (1, 'Test');
INSERT INTO message_areas (name) VALUES ('Work');
