Create table measureunit (
id SERIAL PRIMARY KEY,
name TEXT
);

INSERT INTO measureunit (name)
VALUES
('kg'), ('l')
;

CREATE TABLE ingredients (
id SERIAL PRIMARY KEY,
ingredient TEXT,
price NUMERIC(6, 2),
amount NUMERIC(6, 4),
measureunit_id INT NOT NULL REFERENCES measureunit(id),
priceperunit NUMERIC GENERATED ALWAYS AS (price / amount) STORED
);

INSERT INTO ingredients (ingredient, price, amount, measureunit_id)
VALUES
('pipari', 1.5, 0.3, 1),
('punaiset linssit', 1.4, 0.4, 1),
('punaviini', 14.2, 0.75, 2),
('pecorino', 3.8, 0.180, 1),
('greippimehu', 2.2, 1, 2)
;

CREATE TABLE recipes (
id SERIAL PRIMARY KEY,
name TEXT
);

CREATE TABLE recipes_ingredients (
recipe_id INT REFERENCES recipes(id),
ingredient_id INT REFERENCES ingredients(id),
count INT
);

CREATE TABLE filter (
id SERIAL PRIMARY KEY,
name TEXT
);

insert into filter (name) values ('vegan');

CREATE TABLE filter_ingredient (
filter_id INT REFERENCES filter(id),
ingredient_id INT REFERENCES ingredients(id)
);

insert into filter_ingredient (filter_id, ingredient_id) VALUES (1, 2);
insert into filter_ingredient (filter_id, ingredient_id) VALUES (1, 5);

CREATE TABLE users (
id SERIAL PRIMARY KEY,
username TEXT UNIQUE,
password_hash TEXT
);