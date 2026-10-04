import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--db-user', default='root', show_default=True, help='Database username.')
@click.option('--db-pass', default='root', show_default=True, help='Database password.')
@click.option('--db-host', default='localhost', show_default=True, help='Database host.')
@click.option(
    '--db-port',
    type=click.IntRange(1, 65535),
    default=5432,
    show_default=True,
    help='Database port.',
)
@click.option('--db-name', default='ny_taxi', show_default=True, help='Database name.')
@click.option('--year', type=int, default=2021, show_default=True, help='Taxi data year.')
@click.option('--month', type=click.IntRange(1, 12), default=1, show_default=True, help='Taxi data month.')
@click.option('--target-table', default='yellow_taxi_data', show_default=True, help='Destination table name.')
@click.option(
    '--chunksize',
    type=click.IntRange(min=1),
    default=100000,
    show_default=True,
    help='Rows per insert batch.',
)
def run(
    db_user: str,
    db_pass: str,
    db_host: str,
    db_port: int,
    db_name: str,
    year: int,
    month: int,
    target_table: str,
    chunksize: int,
) -> None:
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    engine = create_engine(f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True

    for df_chunk in tqdm(df_iter, total=14):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("\nTable created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        # print("Inserted:", len(df_chunk))

if __name__ == '__main__':
    run()