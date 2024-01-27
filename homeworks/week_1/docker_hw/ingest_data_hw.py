from sqlalchemy import create_engine
from time import time
import pandas as pd
import argparse
import os


def download_data(url, filename):
    os.system(f"wget {url} -O {filename}")

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name1 = params.table_name1
    table_name2 = params.table_name2
    url1 =params.url1
    url2 =params.url2

    # Downloading CSV file
    download_data(url1, "zones.csv")
    download_data(url2, "green_taxi.csv")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}').connect()
   
    #adding zones_df to postgres database
    zones_df = pd.read_csv("zones.csv")
    zones_df.to_sql(name=table_name1, con=engine, if_exists="replace")

    #adding green_taxi_df to postgres database
    green_taxi_df = pd.read_csv("green_taxi.csv", iterator=True, chunksize=100000, compression="gzip")
    df = next(green_taxi_df)
    df.head(n=0).to_sql(name=table_name2, con=engine, if_exists="replace")
    df.to_sql(name=table_name2, con=engine, if_exists="append")

    for df in green_taxi_df:
        t_start = time()
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.to_sql(name=table_name2, con=engine, if_exists="append")
        t_end = time()
        print('inserted another chunk......., took %.3f seconds' %(t_end - t_start))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument("--user", help='username for postgres')
    parser.add_argument("--password", help='password for postgres')
    parser.add_argument("--host", help='localhost for postgres')
    parser.add_argument("--port", help='port for postgres')
    parser.add_argument("--db", help='database for postgres')
    parser.add_argument("--table_name1", help='name of table1')
    parser.add_argument("--table_name2", help='name of table2')
    parser.add_argument("--url1", help='url1 of the csv')
    parser.add_argument("--url2", help='url1 of the csv')

    args = parser.parse_args()
    main(args)

