## Dockerizing a Data Pipeline App (Python + SQL)

### Architecture Overview

The diagram below illustrates the containerized workflow, where a Docker container runs a Python environment (managed with `uv`) and mounts a persistent host directory for data persistence. <br>
<img src="../screenshots/03/00_concept.png" width="50%"> <br>

### Dockerized Data Pipeline

Create the following Dockerfile file:

```bash
# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["python", "pipeline.py"]

```

then build the image:

> docker build -t test:pandas .

<img src="../screenshots/03/docker-build.png" width="75%"> <br>

We can now run the container and pass an argument to it, so that our pipeline will receive it:

> docker run -it --rm test:pandas {some_number}

<img src="../screenshots/03/docker-run.png" width="50%"> <br>

### Dockerized PostgreSQL

First create the directory in the docker host, then map it:

```bash
mkdir ny_taxi_postgres_data
```

#### Running PostgreSQL in a Container

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \ 
  postgres:18
```

- -e sets environment variables (user, password, database name)
- -v ny_taxi_postgres_data:/var/lib/postgresql creates a named volume

   - Docker manages this volume automatically
   - Data persists even after container is removed
   - Volume is stored in Docker's internal storage

- -p 5432:5432 maps port 5432 from container to host
- postgres:18 uses PostgreSQL version 18 (latest as of Dec 2025)

Named Volume vs Bind Mount

- Named volume (name:/path): Managed by Docker, easier
- Bind mount (/host/path:/container/path): Direct mapping to host filesystem, more control

<img src="../screenshots/03/docker-postgres.png" width="50%"> <br>

<img src="../screenshots/03/docker-postgres-port.png" width="50%"> <br>

#### Install pgcli

I open another terminal di working directory (pipeline), then run the command to install pgcli:

> uv add --dev pgcli

`--dev` flag marks this as a development dependency(not needed in production).

it will add below script in the pyproject.toml file instead of the main `dependencies` section.

```toml
[dependency-groups]
dev = [
    "pgcli>=4.4.0",
]
```

<img src="../screenshots/03/pgcli.png" width="50%"> <br>

#### Connect to Postgres

> uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

- uv run executes a command in the context of the virtual environment
- -h is the host. Since we're running locally we can use localhost.
- -p is the port.
- -u is the username.
- -d is the database name.
- The password is not provided; it will be requested after running the command.
   When prompted, enter the password: root

#### Test Create Table

<img src="../screenshots/03/connect-pgcli.png" width="50%"> <br>