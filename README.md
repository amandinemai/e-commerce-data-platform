🛒 E-commerce Data Platform
Pipeline de données end-to-end pour l'analyse e-commerce, intégrant Salesforce Marketing Cloud, BigQuery, dbt, Airflow et un pipeline CI/CD avec GitHub Actions.
---
📐 Architecture
```
Salesforce MC  ──┐
E-commerce API ──┼──▶  BigQuery (raw)  ──▶  dbt (staging → marts)  ──▶  Looker Studio
CSV simulés    ──┘         ▲                        ▲
                           │                        │
                        Airflow DAG          GitHub Actions CI/CD
```
Couches de données (pattern Medallion)
Couche	Description
`raw`	Données brutes ingérées sans transformation
`staging`	Nettoyage, typage, renommage des colonnes
`marts`	Modèles analytiques finaux (faits & dimensions)
---
🗂️ Structure du projet
```
ecommerce-data-platform/
├── .github/
│   └── workflows/
│       └── dbt_ci.yml          # Pipeline CI/CD
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
├── ingestion/
│   ├── salesforce_mc/
│   └── ecommerce_api/
├── data/
│   └── seed/                   # CSV simulés
├── docs/
│   └── architecture.md
├── .env.example
├── requirements.txt
└── README.md
```
---
⚙️ Prérequis
Python 3.8+
Google Cloud SDK (`gcloud`)
Un projet GCP avec BigQuery activé
Un compte GitHub
---
🚀 Installation
1. Cloner le repo
```bash
git clone https://github.com/TON_USERNAME/ecommerce-data-platform.git
cd ecommerce-data-platform
```
2. Créer l'environnement virtuel
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```
3. Installer les dépendances
```bash
pip install -r requirements.txt
```
4. Authentification Google Cloud
```bash
gcloud auth login
gcloud config set project TON_PROJECT_ID
gcloud auth application-default login
```
5. Configurer dbt
```bash
cd dbt
dbt debug       # vérifie la connexion BigQuery
dbt deps        # installe les packages dbt
```
---
▶️ Lancer le pipeline
Ingestion des données brutes
```bash
python ingestion/load_to_bq.py
```
Transformation dbt
```bash
cd dbt
dbt run         # exécuter les modèles
dbt test        # lancer les tests qualité
dbt docs generate && dbt docs serve   # documentation interactive
```
Orchestration Airflow
```bash
airflow db init
airflow webserver --port 8080
airflow scheduler
```
---
🧪 Tests qualité (dbt)
Les tests suivants sont configurés sur chaque modèle :
Test	Modèle	Colonne
`unique`	`fct_orders`	`order_id`
`not_null`	`fct_orders`	`order_id`, `order_amount`
`not_null`	`dim_customers`	`customer_id`, `email`
`accepted_values`	`stg_orders`	`order_status`
```bash
# Lancer uniquement les tests
dbt test

# Lancer les tests sur un modèle spécifique
dbt test --select fct_orders
```
---
🔄 CI/CD — GitHub Actions
Le pipeline CI/CD se déclenche automatiquement sur chaque pull request vers `main` :
Installation de dbt
Authentification GCP via secret GitHub
`dbt run` sur l'environnement `ci`
`dbt test` — bloque le merge si un test échoue
Secrets GitHub à configurer :
```
GCP_SA_KEY   →  Clé JSON du service account GCP
```
---
📊 Modèles dbt principaux
Facts
Modèle	Description
`fct_orders`	Toutes les commandes avec montant, statut, date
`fct_revenue`	Revenus agrégés par jour / pays / catégorie
`fct_email_events`	Événements Salesforce MC (open, click, bounce)
Dimensions
Modèle	Description
`dim_customers`	Profil client enrichi
`dim_products`	Catalogue produits
`dim_campaigns`	Campagnes marketing Salesforce MC
---
🛠️ Stack technique
Outil	Rôle
BigQuery	Data warehouse cloud
dbt Core	Transformation & modélisation SQL
Airflow	Orchestration du pipeline
Salesforce MC	Source CRM / marketing
GitHub Actions	CI/CD automatisé
Looker Studio	Visualisation & dashboards
Python	Scripts d'ingestion
---
📬 Contact
Projet réalisé dans le cadre d'un portfolio Data Engineering.  
Amandine Mai LE — [linkedin.com/in/amandinemai](https://www.linkedin.com/in/amandinemai-le/) — amandinemai.le4@gmail.com