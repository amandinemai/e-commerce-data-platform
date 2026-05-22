# 🛒 E-commerce Data Platform

End-to-end data pipeline for e-commerce analytics, integrating **data from CSV**, **BigQuery**, **dbt**, **Airflow** and a **CI/CD** pipeline with GitHub Actions.

---

## 📐 Architecture

```

Simulated CSV ────▶  BigQuery (raw)  ──▶  dbt (staging → marts)  ──▶  Looker 
                           ▲                        ▲
                           │                        │
                        Airflow DAG          GitHub Actions CI/CD
```

### Data layers (Medallion pattern)

| Layer | Description |
|-------|-------------|
| `raw` | Raw ingested data, no transformation |
| `staging` | Cleaning, casting, column renaming |
| `marts` | Final analytical models (facts & dimensions) |

---

## 🗂️ Project structure

```
ecommerce-data-platform/
├── .github/
│   └── workflows/
│       └── dbt_ci.yml          # CI/CD pipeline
├── airflow/
│   └── dags/
│       └── ecommerce_pipeline.py
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/            # stg_orders, stg_customers...
│   │   ├── intermediate/
│   │   └── marts/              # fct_orders, dim_customers...
│   └── tests/
├── data/
│   └── seed/                   # Simulated CSV files
├── docs/
│   └── architecture.md
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.8+
- Google Cloud SDK (`gcloud`)
- A GCP project with BigQuery enabled
- A GitHub account

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/amandinemai/e-commerce-data-platform.git
cd ecommerce-data-platform
```

### 2. Create the virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Google Cloud authentication

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

### 5. Configure dbt

```bash
cd dbt
dbt debug       # check BigQuery connection
dbt deps        # install dbt packages
```

---

## ▶️ Running the pipeline

### Raw data ingestion

```bash
python ingestion/load_to_bq.py
```

### dbt transformation

```bash
cd dbt
dbt run         # run models
dbt test        # run data quality tests
dbt docs generate && dbt docs serve   # interactive documentation
```

### Airflow orchestration

```bash
airflow db init
airflow webserver --port 8080
airflow scheduler
```

---

## 🧪 Data quality tests (dbt)

The following tests are configured on each model:

| Test | Model | Column |
|------|-------|--------|
| `unique` | `fct_orders` | `order_id` |
| `not_null` | `fct_orders` | `order_id`, `order_amount` |
| `not_null` | `dim_customers` | `customer_id`, `email` |
| `accepted_values` | `stg_orders` | `order_status` |

```bash
# Run all tests
dbt test

# Run tests on a specific model
dbt test --select fct_orders
```

---

## 🔄 CI/CD — GitHub Actions

The CI/CD pipeline triggers automatically on every **pull request** to `main`:

1. Install dbt
2. Authenticate to GCP via GitHub secret
3. `dbt run` on the `ci` environment
4. `dbt test` — blocks the merge if any test fails

**GitHub secrets to configure:**

```
GCP_SA_KEY   →  JSON key of the GCP service account
```

---

## 📊 Main dbt models

### Facts

| Model | Description |
|-------|-------------|
| `fct_orders` | All orders with amount, status, date |
| `fct_revenue` | Revenue aggregated by day / country / category |
| `fct_email_events` | Salesforce MC events (open, click, bounce) |

### Dimensions

| Model | Description |
|-------|-------------|
| `dim_customers` | Enriched customer profile |
| `dim_products` | Product catalog |
| `dim_campaigns` | Salesforce MC marketing campaigns |

---

## 🛠️ Tech stack

| Tool | Role |
|------|------|
| **BigQuery** | Cloud data warehouse |
| **dbt Core** | SQL transformation & modelling |
| **Airflow** | Pipeline orchestration |
| **GitHub Actions** | Automated CI/CD |
| **Looker Studio** | Visualisation & dashboards |
| **Python** | Ingestion scripts |

---

## 📬 Contact

Project built as part of a Data Engineering portfolio.  
Amandine Mai LE — [linkedin.com/in/amandinemai](https://www.linkedin.com/in/amandinemai-le/) — amandinemai.le4@gmail.com
