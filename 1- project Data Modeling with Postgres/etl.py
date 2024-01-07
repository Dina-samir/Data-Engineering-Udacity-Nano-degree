import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function is responsible for
                 - Reads json file of song data
                 - Insert selected columns ('song_id','title','artist_id','year','duration') to songs table
                 - Insert selected columns ('artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude') to artists table

    Arguments:
                 - cur: cursor to sparkifydb
                 - filepath: The path of song data 
        
    Returns: 
                  - None
    """
    # open song file
    df  = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()

    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data  = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()

    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: 
                 - Reads and processes a single file from log_file
         
     Arguments:
                - cur: cursor to sparkifydb
                - filepath: The path of log data 
        
    Returns: 
                - None
    """
    # open log file
    df =  pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page=='NextSong']

    # convert timestamp column to datetime
    t =  pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data =  (df['ts'].tolist(),t.dt.hour.values.tolist(), t.dt.day.values.tolist(), 
             t.dt.week.values.tolist(),t.dt.month.values.tolist(), t.dt.year.values.tolist(), 
             t.dt.weekday.values.tolist())
    column_labels = ('Timestamp','hour', 'day','week','month','year','weekday')
    time_df =  pd.DataFrame(list(time_data), index = list(column_labels)).transpose()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender' , 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function is responsible for process all json files in the path
    Arguments:
            - cur: cursor to sparkifydb
            - conn: connection to sparkifydb
            - filepath: The path of song data or log data
            - func: function name of function that will read and process the file
        
    Returns: 
           - None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Description: This function is responsible for 
                 - Connect to database sparkifydb
                 - Call process_data fuction to read and process both song_file and log_file
    Arguments: 
                 - None
            
    Returns:
                 - None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()