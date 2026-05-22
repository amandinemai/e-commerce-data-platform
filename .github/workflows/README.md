# 🔄 CI/CD Pipeline — GitHub Actions

![dbt CI](https://github.com/TON_USERNAME/ecommerce-data-platform/actions/workflows/dbt_ci.yml/badge.svg)

Automated CI/CD pipeline that triggers on every **pull request** and **push** to `main`. It runs dbt models and tests against a dedicated BigQuery CI environment.

---

## ⚙️ How it works

Every time code is pushed to `main` or a pull request is opened, GitHub Actions automatically:

1. Sets up a Python environment
2. Installs dbt-bigquery
3. Authenticates to Google Cloud using a service account key
4. Creates a dedicated `dbt_ci` dataset in BigQuery
5. Runs `dbt seed` to load simulated data
6. Runs `dbt run` to build all models
7. Runs `dbt test` to validate data quality — **blocks merge if any test fails**

---

## 🗂️ Workflow file

```
.github/
└── workflows/
    └── dbt_ci.yml
```

---

## 🔐 GitHub Secrets configuration

The pipeline requires one secret to authenticate to Google Cloud:

| Secret | Description |
|--------|-------------|
| `GCP_SA_KEY` | JSON key of the GCP service account with BigQuery Admin role |

### How to add the secret

1. Go to your GitHub repo → **Settings**
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GCP_SA_KEY`
5. Value: paste the full content of your service account JSON key file

---

## 🌍 Environments

| Environment | Dataset | Trigger |
|-------------|---------|---------|
| `dev` | `dbt_dev` | Local development |
| `ci` | `dbt_ci` | GitHub Actions (automatic) |
| `prod` | `dbt_prod` | Manual / scheduled (coming soon) |

---

## 📋 Pipeline steps

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
```

| Step | Action | Description |
|------|--------|-------------|
| 1 | `actions/checkout@v3` | Clone the repository |
| 2 | `actions/setup-python@v4` | Set up Python 3.11 |
| 3 | `pip install dbt-bigquery` | Install dbt adapter |
| 4 | Create GCP key file | Write secret to `/tmp/gcp_key.json` |
| 5 | Create dbt profiles | Generate `~/.dbt/profiles.yml` for CI |
| 6 | `dbt deps` | Install dbt packages |
| 7 | `dbt seed` | Load simulated CSV data |
| 8 | `dbt run` | Build all models |
| 9 | `dbt test` | Run data quality tests |
