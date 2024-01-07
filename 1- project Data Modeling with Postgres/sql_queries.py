# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = 'DROP TABLE IF EXISTS users'
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays(
        songplay_id SERIAL PRIMARY KEY, 
        start_time BIGINT NOT NULL,
        user_id INT NOT NULL, 
        level VARCHAR, 
        song_id VARCHAR, 
        artist_id VARCHAR, 
        session_id INT, 
        location VARCHAR, 
        user_agent VARCHAR,

        UNIQUE (start_time, user_id, song_id, artist_id)
    );
    """)

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY ,
        first_name VARCHAR,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR);

    """)

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
            song_id varchar  PRIMARY KEY,
            title VARCHAR NOT NULL, 
            artist_id varchar NOT NULL,
            year INT, 
            duration FLOAT NOT NULL);
    """)

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id varchar  PRIMARY KEY,
        name varchar NOT NULL, 
        location varchar,
        latitude FLOAT,
        longitude FLOAT);
    """)

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time( 
        start_time BIGINT PRIMARY KEY,
        hour INT, 
        day INT, 
        week INT, 
        month INT, 
        year INT, 
        weekday INT);
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (start_time, user_id, song_id, artist_id) DO UPDATE
    SET 
        level = EXCLUDED.level, 
        session_id = EXCLUDED.session_id, 
        location = EXCLUDED.location, 
        user_agent = EXCLUDED.user_agent;
    """)

user_table_insert = ("""
    INSERT INTO users (user_id, first_name,last_name, gender,level) 
            VALUES(%s,%s,%s,%s,%s)
                    ON CONFLICT DO NOTHING

""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration) 
                VALUES(%s,%s,%s,%s,%s)
                        ON CONFLICT DO NOTHING

""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)  
                VALUES(%s,%s,%s,%s,%s)
                        ON CONFLICT DO NOTHING

""")


time_table_insert = ("""
    INSERT INTO time(start_time, hour, day, week, month, year, weekday) 
               VALUES(%s,%s,%s,%s,%s,%s,%s)
                       ON CONFLICT DO NOTHING

""")

# FIND SONGS

song_select = (""" SELECT song_id, songs.artist_id FROM songs JOIN artists
                                                  ON songs.artist_id = artists.artist_id 
                                                  WHERE title = %s AND name = %s AND duration = %s""")

# QUERY LISTS
#!python create_tables.py
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]