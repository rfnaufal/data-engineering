# Workflow Orchestration

In the previous module, I learned how to use Docker and docker-compose to build containerized data pipelines with PostgreSQL, networking, and persistent storage.

In this module, we will start developing the workflow orchestration using Kestra.  
We will reuse the existing `docker-compose.yaml` with some adjustments to support Kestra.


## Workflow Orchestration Concept

In data engineering, workflow orchestration referes to the automation and coordination of tasks that 

process and move data across system. Instead of manually running jobs one-by one, orchestration 

ensure that:
- taks run in the right order
- dependencies between tasks are handled

this of orchestration as conductor of a data pipeline. 

Kestra position as workflow orchestration that can build workflow as code, on code or with AI.
<img src="guide/ss/diagram.png" width="75%"> 

## 📂 Module Resources

- 📝 Homework: https://github.com/rfnaufal/data-engineering/blob/main/02-workflow-orchestration/guide/99_homework.md
- 🛠 Working Directory: https://github.com/rfnaufal/data-engineering/tree/main/pipeline
