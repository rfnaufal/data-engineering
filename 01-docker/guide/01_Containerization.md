## Containerization

### Create Repository

```sh
gh repo create data-engineering --public
```

```sh
# Navigate to existing project Directory
cd /Users/{username}/Github/Data-Engineering

```

```sh
echo "# data-engineering" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/rfnaufal/data-engineering.git
git push -u origin main
```

### Create .gitignore

```bash
touch .gitignore
vi .gitignore
```

```gitignore
# secrets
.env
*.key.json
orchestration/kestra/secrets/

# data (do not commit)
data/
*.parquet
*.csv
*.jsonl

# python
__pycache__/
.ipynb_checkpoints/
.venv/

# terraform
**/.terraform/
*.tfstate
*.tfstate.*
crash.log

# kestra (optional local state)
.kestra/
```

```sh
git add .gitignore
git commit -m "chore: add gitignore"
git push
```

### Create Codespace

On GitHub: <br>
Open repo → Code → Codespaces → Create codespace on main <br>

To open from VS Code: <br>
Go to GitHub repo <br>
Click Code <br>
Go to Codespaces tab <br>
Click Open in Visual Studio Code <br>
it will require Github Codespaces extensions in VS code.

<img src="../screenshots/1 CS to VSCode.png" width="75%"> <br>

then check the terminal and run docker<br>
<img src="../screenshots/2 VScode.png" width="75%"> <br>

### Managing Containers

Run docker access to bash

> docker run -it --entrypoint=bash python:3.13.11-slim

<img src="../screenshots/3 docker-python-bash.png" width="75%"> <br>

Show all docker status

> docker ps -a

Get all docker id

> docker ps -aq

To delete containers

> docker rm \`docker ps -aq\`

<img src="../screenshots/4 docker.png" width="75%"> <br>

Map Directory to container

> docker run -it --rm -v $(pwd)/test:/app/test --entrypoint=bash python:3.13.11-slim

Note: I add --rm so When the container exits, delete the container automatically.
<img src="../screenshots/5 map volume.png" width="75%"> <br>