## Containerization and Infrastructure as Code

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

https://miniature-space-waddle-vjqr94gw7j2x4wg.github.dev/