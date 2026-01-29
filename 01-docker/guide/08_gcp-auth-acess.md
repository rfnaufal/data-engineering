## GCP Overview

### Initial Setup

- Install gcloud and Terraform using Homebrew
- Navigate to working Directory
- Create .gitignore

#### Authentication

```sh
gh auth login
gcloud alpha projects update {PROJECT_ID} --name="data-playground"
```

```bash
gcloud projects list 
```

Setup service account :

- Grant `viewer` role
- download service-account-key(.json) for auth
- place with the under env folder:

```ini
gcp-terraform-data/
│
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   └── variables.tf
│
├── env/
│   └── gcp/
│       └── service-account.json   👈 put it here
│
└── .gitignore
```

```bash
# From your repo root (gcp-terraform-data/):

# set environment variable to point to your downloadable GCP Keys
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/env/gcp/{service-account-key}.json"
# Activate the service account first
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
# Set the project
gcloud config set project data-playground 
# Verify active account
gcloud auth list 
# Verify project access
gcloud projects list 
```

#### Setup for Access

1. **Service Account IAM Roles.** *You do this ONCE per project (or when permissions change)*

   - Identify the service account email
   - click edit principal for your service account
   - add these roles in addition to viewer:

      - Storage Admin
      - Storage Object Admin
      - Bigquery Admin

      | Role                 | Why Terraform Needs It   |
      | -------------------- | ------------------------ |
      | Viewer               | Read project state       |
      | Storage Admin        | Create buckets           |
      | Storage Object Admin | Manage objects/folders   |
      | BigQuery Admin       | Create datasets & tables |

2. Enable Required APIs:

   - Identity and Access Management (IAM) API
   - IAM Service Account Credentials API

      | API                                  | Why                 |
      | ------------------------------------ | ------------------- |
      | IAM API                              | Permission handling |
      | IAM Service Account Credentials API  | Auth tokens         |
      | (usually auto-enabled but important) |                     |
      | Cloud Storage API                    | Bucket creation     |
      | BigQuery API                         | Dataset creation    |

**Summary**

To successfully deploy infrastructure with Terraform on GCP, three layers must be correctly configured:

| Layer              | What it does                              |
| ------------------ | ----------------------------------------- |
| IAM roles          | What the service account is allowed to do |
| APIs enabled       | What GCP services exist                   |
| Export credentials | Who Terraform acts as                     |

All three are required for Terraform to create and manage cloud resources.