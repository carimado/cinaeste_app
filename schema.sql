-- DATABASE: cinaeste
-- TABLES: users, watch_list, top_movies, reviews

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    f_name VARCHAR(50) NOT NULL,
    l_name VARCHAR(50),
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    bio TEXT,
    avatar TEXT
);

-- DROP TABLE IF EXISTS watch_list CASCADE;
-- CREATE TABLE watch_list (
--     list_id SERIAL PRIMARY KEY,
--     user_id INTEGER,
--         CONSTRAINT fk_user_id
--             FOREIGN KEY (user_id)
--                 REFERENCES users(id),
--     title TEXT NOT NULL,
--     description TEXT,
--     movie_name TEXT NOT NULL
-- );

DROP TABLE IF EXISTS fave_movies CASCADE;
CREATE TABLE fave_movies (
    fave_id SERIAL PRIMARY KEY,
    user_id INTEGER,
        CONSTRAINT fk_user_id
            FOREIGN KEY (user_id)
                REFERENCES users(id),
    movie_id TEXT NOT NULL,
    movie_title TEXT NOT NULL,
    movie_poster TEXT NOT NULL
);

DROP TABLE IF EXISTS watch_list CASCADE;
CREATE TABLE watch_list (
    watch_list_id SERIAL PRIMARY KEY,
    user_id INTEGER,
        CONSTRAINT fk_user_id
            FOREIGN KEY (user_id)
                REFERENCES users(id),
    watch_list_name TEXT NOT NULL,
    watch_list_description TEXT
);

DROP TABLE IF EXISTS watch_list_movies CASCADE;
CREATE TABLE watch_list_movies (
    watch_list_movie_id SERIAL PRIMARY KEY,
    watch_list_id INTEGER,
        CONSTRAINT fk_watch_list_id
            FOREIGN KEY (watch_list_id)
                REFERENCES watch_list(watch_list_id),
    movie_id TEXT
);