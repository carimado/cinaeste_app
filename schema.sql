-- DATABASE: cinaeste
-- TABLES: users, watch_list, top_movies, reviews

-- DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    f_name VARCHAR(50) NOT NULL,
    l_name VARCHAR(50),
    bio TEXT,
    avatar TEXT
);

-- DROP TABLE IF EXISTS users;
CREATE TABLE watch_list (
    list_id SERIAL PRIMARY KEY,
    user_id INTEGER,
        CONSTRAINT fk_user_id
            FOREIGN KEY (user_id)
                REFERENCES users(id),
    title TEXT NOT NULL,
    description TEXT,
    movie_name TEXT NOT NULL
);

-- DROP TABLE IF EXISTS fave_movies;
CREATE TABLE fave_movies (
    fave_id SERIAL PRIMARY KEY,
    user_id INTEGER,
        CONSTRAINT fk_user_id
            FOREIGN KEY (user_id)
                REFERENCES users(id),
    movie_name TEXT NOT NULL
);