import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format, dayofweek
from pyspark.sql.types import TimestampType

#Set AWS credentials
config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Description: This function is responsible for creating and returning a Spark session
    
    Arguments: None
     
    Returns: spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Description: This function is responsible for extracting song data json files from S3 and writing result in parquet in S3
    
    Arguments: 
            spark      : spark session, the entry point to programming Spark.
            input_data : input path for json files in S3 bucket.
            output_data: output path for parquet files in S3 bucket.
     
    Returns: 
            None
    """
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*/"
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table =  df.select(["song_id", "title", "artist_id", "year", "duration"]).distinct()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(os.path.join(output_data, 'songs'),mode="overwrite", partitionBy=['year', 'artist_id'])

    # extract columns to create artists table
    artists_table  = df.select(["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]).distinct()

    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists'),mode="overwrite", partitionBy=['artist_id'] )



def process_log_data(spark, input_data, output_data):
    """
    Description: This function is responsible for extracting song data log files from S3 and writing result in parquet in S3
    
    Arguments: 
            spark      : spark session, the entry point to programming Spark.
            input_data : input path for json files in S3 bucket.
            output_data: output path for parquet files in S3 bucket.
     
    Returns: 
            None
    """
    # get filepath to log data file
    log_data  = input_data + "log_data/*/*/*.json"


    # read log data file
    log_df = spark.read.json(log_data)
    
    # filter by actions for song plays
    log_df = log_df.filter(log_df.page=="NextSong")

    # extract columns for users table    
    users_table = log_df.select(["userId", "firstName", "lastName", "gender", "level"]).drop_duplicates(subset=['userId'])
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users'))


    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x : datetime.utcfromtimestamp(int(x)/1000), TimestampType())
    log_df = log_df.withColumn("start_time", get_timestamp("ts"))
    
    # extract columns to create time table
    time_table = log_df.withColumn("hour",hour("start_time"))\
                    .withColumn("day",dayofmonth("start_time"))\
                    .withColumn("week",weekofyear("start_time"))\
                    .withColumn("month",month("start_time"))\
                    .withColumn("year",year("start_time"))\
                    .withColumn("weekday",dayofweek("start_time"))\
                    .select("start_time","hour", "day", "week", "month", "year", "weekday").drop_duplicates(subset=['start_time'])

    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(os.path.join(output_data, 'time'),mode="overwrite", partitionBy=['year', 'month'])


    # read in song data to use for songplays table
    song_df = spark.read.json(input_data+'song_data/*/*/*/*.json')
 

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = log_df.join(song_df,(log_df.song == song_df.title) & (log_df.artist == song_df.artist_name) & (log_df.length == song_df.duration), how='inner').distinct() \
                        .select("userId", "start_time", "song_id", "artist_id", "level", "sessionId", "location", "userAgent" ) \
                        .withColumn("songplay_id",monotonically_increasing_id()) \
                        .withColumn("month",month("start_time")) \
                        .withColumn("year",year("start_time")) \
                        .withColumnRenamed("userId","user_id")        \
                        .withColumnRenamed("sessionId","session_id")  \
                        .withColumnRenamed("userAgent", "user_agent")


    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(os.path.join(output_data, "songplays"), mode="overwrite", partitionBy=["year","month"])


def main():
    """
    Description: This function is responsible for running the ETL to process the song_data and the log_data files and save result to s3

    Arguments: None
     
    Returns: None
    """
    # Create a Spark Session
    spark = create_spark_session()
    
    #paths to input and output data
    input_data = "s3a://udacity-dend/"
    #the created bucket name udacity-sparkify-data-lake to store all parquet files
    output_data  = "s3a://udacity-sparkify-data-lake/" 
    
    #run ELT process
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)
    
    spark.stop()

if __name__ == "__main__":
    main()
