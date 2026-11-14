# carbapp

Application Android de carte des prix des carburants en France.

## Pipeline de données
`script.py` télécharge chaque jour le CSV des prix (data.gouv.fr), le nettoie et le charge dans BigQuery.
Planification : GitHub Actions (`.github/workflows/data_pipeline.yml`).
Secret requis : `GCP_CREDENTIALS_JSON` (clé JSON du compte de service).
