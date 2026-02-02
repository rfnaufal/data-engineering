## Dockerizing Kestra

### Create Volumes for Postgres and Kestra

# Navigate to the existing project directory
cd /Users/{username}/Github/Data-Engineering/pipeline

Create two folders:
- kestra_postgres_data
- kestra_data

<img src="../screenshots/01/3 docker-python-bash.png" width="75%"> <br>

In the `docker-compose.yaml`, we will add a container for Kestra along with its configuration.

To do this, we need to replace the `docker-compose.yaml` from Module 2 in the working directory.  
Before that, I copied the previous `docker-compose.yaml` file into the `01-docker` folder.

run 'docker-compose up` to run docker