# SQL

We will convert data to sql:

https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

### Create Jupyter Notebook

Create new jupyter notebook and follow previous steps:

`uv run jupyter notebook`

and also ingest the data by running taxi_ingest container.

<img src="../screenshots/07/ingest-data.png" width="75%"> <br>

### Load CSV to Database

<img src="../screenshots/07/download-file.png" width="75%"> <br>

When I tried to load the CSV file into the database, I encountered the error below.

It turns out SQLAlchemy is required, because `df_zones.to_sql()` needs a database engine/connection layer to communicate with PostgreSQL.

Note:
I already installed sqlalchemy and psycopg2-binary in the previous steps. The issue was solved after creating the SQLAlchemy engine using the code below:

```sql
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

```

<img src="../screenshots/07/prereq.png" width="75%"> <br>

<img src="../screenshots/07/rows.png" width="75%"> <br>

265 = total number of zone records in your df_zones dataset

- `len(df_zones)` → returns the number of rows in the DataFrame

- `df_zones.shape[0]` → also returns the number of rows (shape = (rows, columns))

### Test Query

<img src="../screenshots/07/test-query.png" width="75%"> <br>

## JOINS

SQL JOIN is used to combine data from two tables based on a related column (key).

In this example, the yellow_taxi_trips table stores trip details, but pickup locations are stored only as IDs. By joining it with the zones 

lookup table, we can convert those IDs into readable location names (Borough and Zone).

Assume:

- yellow_taxi_trips t = trip records (fact table)

- zones z = lookup table (LocationID → Borough / Zone)

- t."PULocationID" = pickup location ID used as the join key

| Join Type           | Meaning (simple)                       | Keeps rows from trips? | Keeps rows from zones? | When no match       | Sample Query (Taxi + Zones)                                                                                              |
| ------------------- | -------------------------------------- | ---------------------- | ---------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **INNER JOIN**      | Keep only rows where both tables match | Only matched trips     | Only matched zones     | Row is excluded     | `SELECT t.*, z."Zone"<br>FROM yellow_taxi_trips t<br>INNER JOIN zones z<br>  ON t."PULocationID" = z."LocationID";`      |
| **LEFT JOIN**       | Keep all trips, zones added if match   | ✅ Yes (all trips)      | Only matched zones     | Zone columns = NULL | `SELECT t.*, z."Zone"<br>FROM yellow_taxi_trips t<br>LEFT JOIN zones z<br>  ON t."PULocationID" = z."LocationID";`       |
| **RIGHT JOIN**      | Keep all zones, trips added if match   | Only matched trips     | ✅ Yes (all zones)      | Trip columns = NULL | `SELECT t.*, z."Zone"<br>FROM yellow_taxi_trips t<br>RIGHT JOIN zones z<br>  ON t."PULocationID" = z."LocationID";`      |
| **FULL OUTER JOIN** | Keep everything from both tables       | ✅ Yes (all trips)      | ✅ Yes (all zones)      | Missing side = NULL | `SELECT t.*, z."Zone"<br>FROM yellow_taxi_trips t<br>FULL OUTER JOIN zones z<br>  ON t."PULocationID" = z."LocationID";` |

⭐ Quick rule of thumb

- INNER JOIN → normal reporting/analytics (clean matched data)
- LEFT JOIN → safest choice when you don’t want to lose data
- ⚠️ RIGHT JOIN → rarely used --> prefer LEFT JOIN rewrite (changing RIGHT JOIN into LEFT JOIN by swapping tables, without changing the result.)
- FULL OUTER JOIN → auditing and mismatch checks

### Inner Joins

An INNER JOIN combines two tables and returns only the rows that match in both tables based on a related column (key).

📌 Easy way to remember:

- INNER JOIN = keep only matching data
- ✅ Always use explicit JOIN (JOIN ... ON ...) in production / industry projects.
- ⚠️ Avoid implicit joins unless you're reading or maintaining legacy SQL.

| Join style                            | How it’s written                | Where join condition lives | Sample                                                                                             | Pros                                                  | Cons                                                           |
| ------------------------------------- | ------------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------- |
| __Implicit INNER JOIN__ (old style)   | List tables separated by commas | `WHERE` clause             | `sql\nSELECT t.trip_id, z.Zone\nFROM trips t, zones z\nWHERE t.PULocationID = z.LocationID;\n`     | Short syntax                                          | Harder to read, easy to make mistakes, risky for large queries |
| __Explicit INNER JOIN__ (recommended) | Use `JOIN ... ON ...`           | `ON` clause                | `sql\nSELECT t.trip_id, z.Zone\nFROM trips t\nJOIN zones z\n  ON t.PULocationID = z.LocationID;\n` | Clear, safe, easy to maintain, standard in modern SQL | Slightly longer syntax                                         |

#### Implicit Inner Joins

Joining Yellow Taxi table with Zones Lookup table

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t,
    zones zpu,
    zones zdo
WHERE
    t."PULocationID" = zpu."LocationID"
    AND t."DOLocationID" = zdo."LocationID"
LIMIT 100;

```

#### Explicit Inner Joins

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_loc"
FROM
    yellow_taxi_trips t
JOIN
-- or INNER JOIN but it's less used, when writing JOIN, postgreSQL understands implicitly that we want to use an INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

Going forward, I will focus on explicit INNER JOIN syntax, because it is the preferred industry best practice for writing clear and maintainable SQL.