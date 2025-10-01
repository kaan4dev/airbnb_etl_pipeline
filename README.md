# Airbnb ETL Pipeline with PySpark, BigQuery & Airflow

## Project Overview
This project demonstrates an **end-to-end ETL (Extract – Transform – Load) pipeline** built on the **Airbnb dataset**.  
The pipeline extracts raw data, cleans and transforms it with PySpark, loads the results into Google BigQuery, and enables rich SQL analysis.  
Finally, the workflow is orchestrated with Apache Airflow.

---

## Tech Stack
- **Python 3.13**
- **PySpark** → Data cleaning & transformation
- **Google Cloud Storage (GCS)** → Intermediate storage
- **Google BigQuery** → Data warehouse & SQL analytics
- **Apache Airflow** → Orchestration & scheduling
- **Pandas, Matplotlib, Seaborn** → Analysis & visualization (Jupyter Notebook)

---

## 📂 Repository Structure
```

airbnb_etl_pipeline/
│
├── data/
│   ├── raw/                # Raw Airbnb dataset
│   └── processed/          # Cleaned data (post-PySpark)
│
├── src/
│   ├── extract.py          # Extract step
│   ├── transform.py        # Transform step (PySpark)
│   └── load.py             # Load step (BigQuery)
│
├── dags/
│   └── airbnb_etl_dag.py   # Airflow DAG definition
│
├── notebooks/
│   └── analysis.ipynb      # SQL + Python analysis notebook
│
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

````

---



## Data Analysis

Sample SQL queries for analysis in BigQuery:

```sql
-- Total number of rows
SELECT COUNT(*) FROM `airbnb_pipeline.cleaned_listings`;

-- Average price by room type
SELECT room_type, AVG(price) AS avg_price
FROM `airbnb_pipeline.cleaned_listings`
GROUP BY room_type
ORDER BY avg_price DESC;
```

For advanced queries and visualizations, see [notebooks/analysis.ipynb](notebooks/analysis.ipynb).

---

##  Airflow DAG

The ETL pipeline can be orchestrated via Apache Airflow.
DAG file: `dags/airbnb_etl_dag.py`

Run Airflow locally:

```bash
airflow standalone
```

---

## Key Outcomes

With this project, i:

* Built a full ETL pipeline from raw Airbnb data to analytics,
* Performed large-scale data cleaning and feature engineering with PySpark,
* Integrated with Google Cloud Storage and BigQuery,
* Automated the workflow using Airflow,
* Conducted SQL analysis and visualization in Jupyter Notebook.
```
