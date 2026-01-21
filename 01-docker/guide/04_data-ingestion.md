## Data Ingestion

### Install Jupyter

Install Jupyter notebook in the docker host:

```bash
uv add --dev jupyter
```

it will add jupyter in the dependency-group

<img src="../screenshots/04/jupyter.png" width="50%"> <br>

```bash
uv run jupyter notebook
```

after runnning you will got the token, copy the token as shown below:

<img src="../screenshots/04/uv-jupyter.png" width="50%"> <br>

click open the browser, or you also can access from PORTS tab next to TERMINAL.

Then, paste the token

<img src="../screenshots/04/jupyter-token.png" width="50%"> <br>
Now you can access working directory(pipeline folder) in the docker host through Jupyter

<img src="../screenshots/04/jupyter-login.png" width="50%"> <br>

### Use Case: NYC TLC Trip Record Dataset

We will use data from the NYC TLC Trip Record Data website.

Specifically, we will use the Yellow taxi trip records CSV file for January 2021.

This data used to be csv, but later they switched to parquet. We want to keep using CSV because we need to do a bit of extra pre-processing (for the purposes of learning it).

A dictionary to understand each field is available here.

> Note: The CSV data is stored as gzipped files. Pandas can read them directly.

### Ingesting Data into Postgres

In the Jupyter notebook, we will create code to:

- Download the CSV file
- Read it in chunks with pandas
- Convert datetime columns
- Insert data into PostgreSQL using SQLAlchemy

#### Create Jupyter Notebook

We will now create a Jupyter Notebook notebook.ipynb file which we will use to read a CSV file and export it to Postgres.

then run:

```python
import pandas as pd

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)

# Display first rows
df.head()

# Check data types
df.dtypes

# Check data shape
df.shape
```

We have warning here, because Pandas scanned the CSV and found that column index 6 (the 7th column) contains mixed data types.
e.g.:

- some rows look like numbers: 123

- other rows look like text: N/A, -, unknown

- or values have commas: 1,000

- or some rows empty → becomes NaN

So pandas can’t confidently decide the dtype (int, float, string), and warns you.

<img src="../screenshots/04/jupyter-nb.png" width="75%"> <br>

I  use df.info() to quickly confirm:

- dtype problems

- missing values

- dataset shape

<img src="../screenshots/04/df-info.png" width="75%"> <br>

for tpep_pickup_datetime column, it's suppose datetime but currently it's object which means string type. 

<img src="../screenshots/04/dt-problem.png" width="75%"> <br>

#### Convert Datatypes (datetime columns)

run below snippet to forces correct data types

```python
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

df = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates
)

```

<img src="../screenshots/04/force-dt.png" width="75%"> <br>

and now tpep_pickup_datetime column change to datetime.

#### Insert data into PostgreSQL using SQLAlchemy

##### Install SQLAlchemy and psycopg2-binary

from the notebook, run:
```
!uv add sqlalchemy
```

<img src="../screenshots/04/install-alchemy.png" width="75%"> <br>

SQLalchemy added into dependencies in the pyproject.toml

<img src="../screenshots/04/alchemy-pyproject.png" width="75%"> <br>

we also need library
```
!uv add psycopg2-binary
```

##### Create Database Connection

```
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```

##### Get DDL Schema

```
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
```

<img src="../screenshots/04/create-db-connection.png" width="75%"> <br>

##### Create the Table

We will create the table only with the schema, no data yet.

```
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

<img src="../screenshots/04/create-table.png" width="75%"> <br>

connect to Postgres from terminal, ensure in the pipeline folder as working directory then running:
```
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

<img src="../screenshots/04/validate-table.png" width="75%"> <br>

### Ingesting Data in Chunks

Optimize data ingestion with chunks.

We don't want to insert all the data at once. Let's do it in batches and use an iterator for that:

```
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator = True,
    chunksize=100000,
)
```

#### Iterate Over Chunks

```
for df_chunk in df_iter:
    print(len(df_chunk))
```

<img src="../screenshots/04/iterate-chunks.png" width="75%"> <br>

#### Inserting Data

Add library tqdm to show a progress bar while your code is running.
```
!uv add tqdm
```

```
for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

<img src="../screenshots/04/insert-chunk-data.png" width="75%"> <br>

#### Validating the Data

<img src="../screenshots/04/validate-insert-data.png" width="75%"> <br>

### Convert Notebook to Ingestion Script

```
uv run jupyter nbconvert --to=script notebook.ipynb
mv notebook.py ingest_data.py
uv run python ingest_data.py
```

<img src="../screenshots/04/run-ingest-data.png" width="75%"> <br>

We use click library to build command-line tools (CLI apps) easily.

<img src="../screenshots/04/click-library.png" width="75%"> <br>

### Running the Script

The script reads data in chunks (100,000 rows at a time) to handle large files efficiently without running out of memory.

```bash
uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 \
  --month=1 \
  --chunksize=100000
```