from google.cloud import bigquery

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "https://github.com/yousschb/cloud-analytics/blob/main/caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant la clé d'API
client = bigquery.Client(project="caa-assignement-1-417215", credentials=key)

# Exécutez une requête SQL
query = """
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE LOWER(title) LIKE LOWER('terminator%')
"""
query_job = client.query(query)

# Récupérez les résultats de la requête
results = query_job.result()

# Affichez les résultats
for row in results:
    print(row["title"])




