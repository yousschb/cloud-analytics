from google.cloud import bigquery

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Exemple de requête SQL
query = """
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE LOWER(title) LIKE LOWER('terminator%')
"""

# Exécuter la requête
query_job = client.query(query)

# Récupérez les résultats de la requête
results = query_job.result()

# Affichez les résultats
for row in results:
    print(row["title"])
