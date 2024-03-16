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

# Titre de l'application
st.title("Movie Database Search")

# Afficher le champ de recherche pour les titres de films
search_query = st.text_input("Search for movie titles", "")

# Requête SQL pour l'autocomplétion des titres de films
query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE LOWER(title) LIKE LOWER('%{search_query}%')
"""

# Exécuter la requête
query_job = client.query(query)

# Récupérer les résultats de la requête
query_results = query_job.result()

# Afficher les résultats
for row in query_results:
    st.write(row)

