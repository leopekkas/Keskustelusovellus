CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    visibility INTEGER
);
CREATE TABLE message_areas (
    id SERIAL PRIMARY KEY,
    name text,
    user_id INTEGER REFERENCES users
);
CREATE TABLE access_rights (
    message_area_id INTEGER REFERENCES message_areas, user_id INTEGER REFERENCES users
);
INSERT INTO message_areas (id, name) VALUES (1, 'Test');
INSERT INTO message_areas (name) VALUES ('Work');
