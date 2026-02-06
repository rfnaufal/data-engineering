## Load Data Taxi to PostgreSQL(Local Database)

### Preparation
We will use the flow file [`04_postgres_taxi.yaml`](https://github.com/rfnaufal/data-engineering/blob/main/02-workflow-orchestration/flows/04_postgres_taxi.yaml) to process the Yellow and Green Taxi datasets using a local PostgreSQL database running inside a Docker container.

This setup reuses the same database from Module 1, which is defined in the same Docker Compose file as Kestra.

The workflow performs the following steps:

- Extracts CSV data partitioned by year and month
- Creates the required tables
- Loads data into monthly staging tables
- Merges the monthly data into the final destination tables

```mermaid
graph LR
  Start[Select Year & Month] --> SetLabel[Set Labels]
  SetLabel --> Extract[Extract CSV Data]
  Extract -->|Taxi=Yellow| YellowFinalTable[Create Yellow Final Table]:::yellow
  Extract -->|Taxi=Green| GreenFinalTable[Create Green Final Table]:::green
  YellowFinalTable --> YellowMonthlyTable[Create Yellow Monthly Table]:::yellow
  GreenFinalTable --> GreenMonthlyTable[Create Green Monthly Table]:::green
  YellowMonthlyTable --> YellowCopyIn[Load Data to Monthly Table]:::yellow
  GreenMonthlyTable --> GreenCopyIn[Load Data to Monthly Table]:::green
  YellowCopyIn --> YellowMerge[Merge Yellow Data]:::yellow
  GreenCopyIn --> GreenMerge[Merge Green Data]:::green

  classDef yellow fill:#FFD700,stroke:#000,stroke-width:1px;
  classDef green fill:#32CD32,stroke:#000,stroke-width:1px;
```

    <img src="ss/03/05-output-transform-product.png" width="75%"> <br>






