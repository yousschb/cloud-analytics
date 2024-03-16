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

# Zone de texte pour la requête de l'utilisateur
query = st.text_input("Search for movies:", "")

# Bouton pour exécuter la requête
if st.button("Search"):
    # Exécutez la requête SQL en fonction de la recherche de l'utilisateur
    # et affichez les résultats
    # Ajoutez votre logique SQL ici
    # par exemple : query_results = client.query("SELECT * FROM ...")
    # puis affichez les résultats : for row in query_results: st.write(row)
