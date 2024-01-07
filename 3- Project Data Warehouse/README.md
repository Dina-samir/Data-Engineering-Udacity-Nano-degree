# Project: Data Warehouse

## Summary:
Sparkify data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
We are building an ETL pipeline that extracts Sparkify data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights.

## Database Schema:
We created a star schema optimized for queries on song play analysis. This includes the following tables.
#### Fact Table
* songplays - records in event data associated with song plays i.e. records with page NextSong
  songplay_id, start_time, user_id, level, song_id, artist_id,  session_id, location, user_agent
#### Dimension Tables
* users - users in the app
  user_id, first_name, last_name, gender, level
* songs - songs in music database
  song_id, title, artist_id, year, duration
* artists - artists in music database
  artist_id, name, location, lattitude, longitude
* time - timestamps of records in songplays broken down into specific units
  start_time, hour, day, week, month, year, weekday
  
## Files
* create_table.py -> to create your fact and dimension tables for the star schema in Redshift.
* etl.py -> to load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
* sql_queries.py -> to define you SQL statements, which will be imported into the two other files above.
* README.md -> provide discussion on your process and decisions for this ETL pipeline.
* dwh.cfg -> Have S3(import data) and Redshift Cluster (analize data) configuration.


## ETL Process on AWS
* first, we creared user, role and Redshist cluster
* then We created the tables by running 
  (!python create_tables.py) in terminal which uses sql queries in  sql_queries.py
* finally, we loaded staging tables from S3 by copy_table_queries and insertd data to final tables by running (!python etl.py)

## How to run 
!python create_tables.py (Drop and recreate tables)

!python etl.py (Run ETL pipeline)





