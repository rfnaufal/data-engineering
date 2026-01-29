## Terraform

### workflow lifecycle

<img src="../ss/02/01-workflow.png" width="70%">

### TF Files

| File Name           | Purpose                                         | What It Manages                                                   | Why It Exists                                                  |
| ------------------- | ----------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------- |
| `versions.tf`       | Defines Terraform & provider versions           | Terraform engine and Google Cloud provider                        | Prevents breaking changes and ensures consistent environments  |
| `providers.tf`      | Configures GCP connection                       | Authentication, project selection, regional defaults              | Allows Terraform to communicate with GCP APIs                  |
| `variables.tf`      | Declares configurable inputs                    | Project ID, region, bucket names, dataset IDs, environment labels | Makes infrastructure reusable and environment-aware            |
| `main.tf`           | Defines infrastructure resources                | Cloud Storage data lake, BigQuery dataset & tables                | Builds the actual cloud platform                               |
| `outputs.tf`        | Exposes important values                        | Bucket name, dataset ID, resource locations                       | Improves visibility and integration                            |
| `terraform.tfvars`  | Stores environment-specific values (local only) | Project ID, bucket name, dataset ID, environment settings         | Keeps configuration out of code and secrets out of Git         |
| `terraform.tfstate` | Tracks real deployed infrastructure             | Resource IDs, metadata, dependencies                              | Allows Terraform to know what exists and manage changes safely |

**Optional Supporting Files**

| File                  | Purpose                          | Notes                       |
| --------------------- | -------------------------------- | --------------------------- |
| `.gitignore`          | Protects secrets and state files | Prevents credential leaks   |
| `.terraform/`         | Provider binaries & cache        | Auto-generated              |
| `.terraform.lock.hcl` | Provider dependency lock         | Ensures consistent installs |

**Notes:**
- terraform.tfstate is the source of truth for Terraform.

   If you lose it, Terraform no longer knows what infrastructure exists.   

### Step 1 — Authenticate Terraform with GCP

Export the service account credentials so Terraform can access GCP APIs:

`export GOOGLE_APPLICATION_CREDENTIALS="$PWD/env/gcp/{service-account}.json"`

Verify authentication:

`gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"`

`gcloud projects list`

You should see your GCP project listed.

Note:
Because Terraform does NOT automatically reuse what you did in GCP Console, iIt needs credentials in your local shell every time you start a session.

### Step 2 — Configure Environment Variables 
Create terraform.tfvars

```terraform
project_id   = "data-playground-12345"
bucket_name  = "data-playground-12345-datalake-dev"
environment  = "dev"
bq_dataset_id = "datalake"
```

### Step 3 — Initialize Terraform

From Terraform Directory:
```
cd terraform
terraform init
```

**Notes:**

Before I execute the plan I run:

1. `terraform fmt`

    It verifies:

    • Scans all .tf files in the current directory

    • Reformats only the ones with style issues

    • Prints only changed files


    I see  `main.tf` as a result.

        means:

        ✔ main.tf was adjusted

        ✔ others were already formatted correctly

2. I also run `terraform validate` 
    It verifies:

        ✔ Syntax is correct

        ✔ Required variables exist

        ✔ Providers are configured properly

        ✔ References are valid (module.x.output, etc.)

        ✔ No broken expressions

### Step 4 — Preview Infrastructure Changes

`terraform plan -out=tfplan`

- Terraform creates file:
    `terraform/tfplan`

- update .gitignore, add tfplan*
- Review the output to confirm:

    - APIs will be enabled

    - Cloud Storage bucket will be created

    - BigQuery dataset (and tables) will be created
    
    - No resources should be destroyed.

### Step 5 — Deploy Infrastructure

`terraform apply tfplan`

When prompted, type:

`yes`

Terraform will now provision all GCP resources.

### Step 6 — Validate in GCP

**Cloud Storage**

Verify data lake bucket exists in asia-southeast2

Confirm folder structure is created

**BigQuery**

Verify dataset exists in asia-southeast2

### Clean Up

Before destroying, always preview:

`terraform plan -destroy`

To remove all deployed resources:

`terraform destroy`

### Optional : I want to auto-generate resource names for bucket_name

1. Create New file name local.tf
    Inside your terraform/ directory:
    ```
    terraform/
    ├── main.tf
    ├── providers.tf
    ├── variables.tf
    ├── versions.tf
    ├── outputs.tf
    └── locals.tf   👈 add this

    **local.tf**
    locals {
    bucket_name = "${var.project_id}-datalake-${var.environment}"
    }
    ```

2. Update main.tf
    Change your bucket resource from: name = `var.bucket_name` 
    to `name = local.bucket_name`

3. Remove from variables.tf and terraform.tfvars
    Delete:
    ```
    variable "bucket_name" {
        ...
    } ```