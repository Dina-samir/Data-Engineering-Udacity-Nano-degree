import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
      """
    Description: This function is responsible copying staging tables from s3 to cluster
    
    Arguments:
     cur: cursor to cluster database
     conn: connection to cluster database
        
    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description: This function is responsible inserting data to final tables  
    
    Arguments:
     cur: cursor to cluster database
     conn: connection to cluster database
        
    Returns:
        None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Description: This function is responsible for 
    - Reading redshift cluster configuration, connect the cluster and gets cursor to it.  
    - Loading data from S3 to staging database  
    - insert data to final tables
    
    Arguments:
        None

    Returns:
        None
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()