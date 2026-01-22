## PgAdmin

<img src="../screenshots/05/00_concept.png" width="50%"> <br>

### pgAdmin Container

```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
  ```

<img src="../screenshots/05/pgadmin-install.png" width="50%"> <br>

<img src="../screenshots/05/pgadmin-ui.png" width="50%"> <br>

<img src="../screenshots/05/pgadmin-login.png" width="50%"> <br>