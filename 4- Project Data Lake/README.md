# Project: Data Warehouse

## Summary:
Sparkify data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
We are building an ETL pipeline with spark to extracts Sparkify data from S3, processes them using Spark, then loads the data back into S3 in praquet format.

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
  
  
## Data Lake to store extracted dimentional tables
"s3a://udacity-sparkify-data-lake/artists"
"s3a://udacity-sparkify-data-lake/songs"
"s3a://udacity-sparkify-data-lake/time"
"s3a://udacity-sparkify-data-lake/users"
"s3a://udacity-sparkify-data-lake/songplays"
  
## Files
* etl.py -> to load data from S3, process them with spark thn upload to datalake on S3.
* README.md -> provide discussion on your process and decisions for this ETL pipeline.
* dl.cfg -> Have S3(import data) and Redshift Cluster (analize data) configuration.

## How to run 
!python etl.py (Run ETL pipeline)
