from time import time
from sqlalchemy import create_engine
import pandas as pd
import argparse
import os

def main(params):
    # Parameter from argparse
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url =params.url
    csv_name = "output.csv"

    # Downloading CSV file
    os.system(f"wget {url} -O {csv_name}")

    # Ingestion of Data to Database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip')
    df = next(df_iter)

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    #just to add table without inputting data
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    #Injestion of Data to Database
    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk......., took %.3f seconds' %(t_end - t_start))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv')

    args = parser.parse_args()
    main(args)









