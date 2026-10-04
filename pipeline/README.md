# Taxi data ingestion

Run the ingestion script with the default database connection, data period, table, and
batch size:

```bash
uv run python ingest_data.py
```

Override any value with its corresponding option. For example:

```bash
uv run python ingest_data.py --db-host localhost --year 2021 --month 2 --chunksize 50000
```

Use `uv run python ingest_data.py --help` to list all options and their defaults.
