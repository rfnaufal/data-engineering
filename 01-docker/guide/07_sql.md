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

## How to Read an SQL Query (Logical Order)

Here is a visual guide on how to read an SQL query in logical order. Since I don’t frequently work with SQL in my current role, I’m including this as a quick refresher to help me review and understand SQL query structure more effectively.

<img src="../screenshots/07/read-sql.png" width="30%"> <br>

## JOINS

SQL JOIN is used to combine data from two tables based on a related column (key).

In this example, the yellow_taxi_trips table stores trip details, but pickup locations are stored only as IDs. By joining it with the zones

lookup table, we can convert those IDs into readable location names (Borough and Zone).

Assume:

- yellow_taxi_trips t = trip records (fact table)
- zones z = lookup table (LocationID → Borough / Zone)
- t."PULocationID" = pickup location ID used as the join key

| Join Type           | Meaning (simple)                       | Keeps rows from trips? | Keeps rows from zones? | When no match           | Sample Query (Taxi + Zones)                                                                                                                                                |
| ------------------- | -------------------------------------- | ---------------------- | ---------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| __INNER JOIN__      | Keep only rows where both tables match | Only matched trips     | Only matched zones     | Row is __excluded__     | <code>SELECT t._, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>INNER JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code>      |
| __LEFT JOIN__       | Keep all trips, zones added if match   | ✅ Yes (all trips)      | Only matched zones     | Zone columns = __NULL__ | <code>SELECT t._, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>LEFT JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code>       |
| __RIGHT JOIN__      | Keep all zones, trips added if match   | Only matched trips     | ✅ Yes (all zones)      | Trip columns = __NULL__ | <code>SELECT t._, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>RIGHT JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code>      |
| __FULL OUTER JOIN__ | Keep everything from both tables       | ✅ Yes (all trips)      | ✅ Yes (all zones)      | Missing side = __NULL__ | <code>SELECT t._, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>FULL OUTER JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code> |

⭐ Quick rule of thumb

- **INNER JOIN** → Best for normal reporting/analytics (returns only matched rows)
- **OUTER JOIN types** (keep unmatched rows):
  - LEFT JOIN (LEFT OUTER JOIN) → Safest choice when you don’t want to lose trips (unmatched zones become `NULL`)
  - RIGHT JOIN (RIGHT OUTER JOIN) → Rarely used; usually rewritten as LEFT JOIN by swapping table order (same result)
  - FULL OUTER JOIN → Useful for auditing and mismatch checks (keeps everything from both tables)

### Inner Joins

An INNER JOIN combines two tables and returns only the rows that match in both tables based on a related column (key).

📌 Easy way to remember:

- INNER JOIN = keep only matching data
- ✅ Always use explicit JOIN (JOIN ... ON ...) in production / industry projects.
- ⚠️ Avoid implicit joins unless you're reading or maintaining legacy SQL.

| Join style                            | How it’s written                | Where join condition lives | Sample                                                                                                                                              | Pros                                                  | Cons                                                           |
| ------------------------------------- | ------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------- |
| __Implicit INNER JOIN__ (old style)   | List tables separated by commas | `WHERE` clause             | <code>SELECT t.trip_id, z.Zone</code><br><code>FROM trips t, zones z</code><br><code>WHERE t.PULocationID = z.LocationID;</code>                    | Short syntax                                          | Harder to read, easy to make mistakes, risky for large queries |
| __Explicit INNER JOIN__ (recommended) | Use `JOIN ... ON ...`           | `ON` clause                | <code>SELECT t.trip_id, z.Zone</code><br><code>FROM trips t</code><br><code>JOIN zones z</code><br><code>  ON t.PULocationID = z.LocationID;</code> | Clear, safe, easy to maintain, standard in modern SQL | Slightly longer syntax                                         |

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
-- Purpose:
-- Join taxi trip records with the zones lookup table
-- to map pickup/dropoff Location IDs into Borough and Zone information.

SELECT
    -- Trip timestamps from yellow_taxi_trips table
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,

    -- Total fare amount for the trip
    t.total_amount,

    -- CONCAT() combines multiple text values into a single string:
    -- Borough + " | " + Zone
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS pickup_loc,

    -- Same CONCAT() logic for dropoff location
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS dropoff_loc
FROM
    -- Main fact table: each row represents one taxi trip
    yellow_taxi_trips t

    -- Join pickup zones:
    -- JOIN in PostgreSQL is equivalent to INNER JOIN
JOIN zones zpu
    ON t."PULocationID" = zpu."LocationID"

    -- Join dropoff zones (zones table joined again using a different alias)
JOIN zones zdo
    ON t."DOLocationID" = zdo."LocationID"

-- Limit results for preview/testing
LIMIT 100;

```

Going forward, I will focus on explicit INNER JOIN syntax, because it is the preferred industry best practice for writing clear and maintainable SQL.

##### Test Explicit Join with limit

<img src="../screenshots/07/explicit.png" width="75%"> <br>

##### Test Explicit Join without alias

<img src="../screenshots/07/explicit-no-alias.png" width="75%"> <br>

##### Test Explicit Join with WHERE filters

<img src="../screenshots/07/explicit-with-where.png" width="75%"> <br>

### Outer Joins

| Join Type                           | Outer Join? | Keeps rows from trips (`yellow_taxi_trips`)? | Keeps rows from zones (`zones`)? | When no match               | Sample Query                                                                                                                                                               |
| ----------------------------------- | ----------- | -------------------------------------------- | -------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LEFT JOIN** (`LEFT OUTER JOIN`)   | ✅ Yes       | ✅ Yes (all trips)                            | Only matched zones               | Zones columns become `NULL` | <code>SELECT t.*, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>LEFT JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code>       |
| **RIGHT JOIN** (`RIGHT OUTER JOIN`) | ✅ Yes       | Only matched trips                           | ✅ Yes (all zones)                | Trip columns become `NULL`  | <code>SELECT t.*, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>RIGHT JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code>      |
| **FULL OUTER JOIN**                 | ✅ Yes       | ✅ Yes (all trips)                            | ✅ Yes (all zones)                | Missing side becomes `NULL` | <code>SELECT t.*, z."Zone"</code><br><code>FROM yellow_taxi_trips t</code><br><code>FULL OUTER JOIN zones z</code><br><code>  ON t."PULocationID" = z."LocationID";</code> |

#### Left Join

<img src="../screenshots/07/left.png" width="75%"> <br>

#### Right Join

<img src="../screenshots/07/right.png" width="75%"> <br>

## Data Quality Checks

### Checking for NULL Location IDs

<img src="../screenshots/07/null-locationid.png" width="75%"> <br>

### Checking for Location IDs NOT IN Zones Table

<img src="../screenshots/07/locationid-zones.png" width="75%"> <br>