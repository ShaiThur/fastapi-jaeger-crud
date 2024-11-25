CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER
);

INSERT INTO "user"(name, age) VALUES
    ('Jane', 27)