# NYC Yellow Taxi Ingestion Pipeline (Dockerized)

> Data Engineering Zoomcamp (DataTalksClub) · **Module 1.1: Docker**

A containerized, reproducible batch ingestion pipeline. It pulls NYC Yellow Taxi trip data from the web, loads it into PostgreSQL in memory-safe chunks, and exposes it through pgAdmin for SQL exploration. Everything runs with one command and nothing needs to be installed on the host except Docker. This was done as an exercise while learning technologies and important concepts such as virtualization, reproducible environments, isolation, stateless containers, how to preserve data in mounted binds or in named volumes, and how to adjust dependencies properly. All the material and the classes live in the following repo [Docker Module]((https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform)).

## Architecture

```
  NYC Yellow Taxi data (web)
            │  HTTP download
            ▼
┌──────────────────────────────────────── docker compose ─┐
│  ingest container            postgres          pgadmin  │
│  Python + uv   ── chunks ──▶ (taxi tables) ◀── queries ─│
└──────────────────────────────────────────────────────────┘
```

| Service | Role |
|---|---|
| `ingest` | Downloads the dataset and loads it into Postgres in chunks. Runs once and exits. |
| `postgres` | The warehouse. Stores the taxi trips table. |
| `pgadmin` | Browser UI for running queries and inspecting the data. |

## Key design decisions

- **Chunked ingestion.** The source files are large. Reading them whole would exhaust memory, so rows are streamed and inserted in fixed-size batches. Memory use stays flat regardless of file size, which is how production batch jobs are built.
- **Reproducible environments with `uv`.** Python version and dependencies are pinned and resolved by [uv](https://github.com/astral-sh/uv). The image installs from the lockfile, so the container behaves the same on every machine and build.
- **Debian/Ubuntu-based image.** A slim Linux base keeps the image small and predictable, with project dependencies layered on top so rebuilds stay fast through Docker layer caching.
- **Orchestration with Docker Compose.** Service definitions, networking, and environment variables live in one declarative file. Services reach each other by name (for example `postgres:5432`) over the internal Compose network.
- **Plain Python for extraction.** Downloading and parsing the source files is done in vanilla Python, so every step of the data flow is explicit and easy to debug.
- **Version controlled.** The whole project is tracked with Git and hosted on GitHub.

## Tech stack

`Python` · `uv` · `Docker` · `Docker Compose` · `PostgreSQL` · `pgAdmin` · `Git/GitHub` . `pyarrow` . `pandas` . `click` . `sqlalchemy` . `psycopg2`

## Project structure

```
.
├── pipeline/   # ingestion code, Dockerfile, uv project files, compose setup
├── test/       # tests and experiments
├── .gitignore
└── README.md
```

## Getting started

**Prerequisites:** Docker and Docker Compose.

```bash
# 1. Clone
git clone https://github.com/chuckm990/dezc_dtc_mod1_docker.git
cd dezc_dtc_mod1_docker/pipeline

# 2. Build the image and start the stack
docker compose up --build
```

Once the ingest container finishes, open pgAdmin in your browser (the host port is defined in the compose file), register the Postgres server using the credentials from the compose file, and run:

```sql
SELECT COUNT(*) FROM yellow_taxi_data;
```

Tear everything down, including volumes:

```bash
docker compose down -v
```

## What I learned

- Containers are the unit of reproducibility: if it runs in the image, it runs anywhere.
- Streaming data in chunks is the difference between a script and a pipeline.
- Compose turns a multi-service setup into a single versioned file.
- Dependency locking (`uv.lock`) removes "works on my machine" from the conversation.

## A hurdle along the road
 - When trying to establish the container network connection, had an issue with the workspace, which was a virtualized environment as well (inside a docker container), that I overcame using the following line in bash: `sudo iptables-legacy -P FORWARD ACCEPT`. After this, all connections worked just fine, and containers were able to interact with each other inside the pipeline network.

## Roadmap

- [x] **Module 1.1:** Docker, Docker Compose, Postgres ingestion
- [ ] **Module 1.2:** Infrastructure as Code with Terraform
- [ ] Parameterize the pipeline (month/year via CLI arguments)
- [ ] Add data validation and idempotent loads

## Acknowledgements

Built as part of the free [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by [DataTalksClub](https://datatalks.club/).
