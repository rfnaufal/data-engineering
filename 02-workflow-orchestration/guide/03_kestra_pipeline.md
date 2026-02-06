## Build Data Pipeline Kestra

### Preparation
We will use [`03_getting_started_data_pipeline`](https://github.com/rfnaufal/data-engineering/blob/main/02-workflow-orchestration/flows/03_getting_started_data_pipeline.yaml) to build our first pipeline.

## Pipeline

here is the ETL process within the pipeline. as input we choose the columns (brand, price).

<img src="ss/03/01.png" width="75%">

there are 3 taskId :
```mermaid
graph LR
  Extract[Extract Data via HTTP REST API] --> Transform[Transform Data in Python]
  Transform --> Query[Query Data with DuckDB]
```

1. Extract 
    Download raw products JSON
2. Tranform
    Python filters it into products.json
    <img src="ss/03/02-ET.png" width="75%">
3. Query
    DuckDB computes average price per brand and stores the result
    <img src="ss/03/03-Query.png" width="75%">
    the actual query:
    ```sql
    SELECT brand, round(avg(price), 2) as avg_price
    FROM read_json_auto('{{workingDir}}/products.json')
    GROUP BY brand
    ORDER BY avg_price DESC;
    ```

    Translation:

    - read your products.json
    - group by brand
    - compute average price
    - sort from highest avg price to lowest
    
    So the end product is basically:

    “Which brands are expensive on average?”

    with `fetchType: STORE` means it's store the result.

    here are the outputs:

        <img src="ss/03/04-output-extract.png" width="75%"> <br>
        <img src="ss/03/04-output-query.png" width="75%"> <br>
        <img src="ss/03/04-output-transform-data.png" width="75%"> <br>
        <img src="ss/03/04-output-transform-product.png" width="75%"> <br>






