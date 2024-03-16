from google.cloud import bigquery
import streamlit as st

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


# Liste déroulante pour sélectionner la langue
language = st.selectbox("Select language", ["English", "French", "German", "Spanish", "Italian"])

# Requête SQL pour filtrer par langue
query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE language = '{language}'
"""

# Exécuter la requête
query_job = client.query(query)

# Récupérer les résultats de la requête
query_results = query_job.result()

# Afficher les résultats
for row in query_results:
    st.write(row)


# Liste déroulante pour sélectionner le genre de film
genre = st.selectbox("Select genre", ["Action", "Comedy", "Drama", "Horror", "Science Fiction"])

# Requête SQL pour filtrer par genre de film
query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE genres LIKE '%{genre}%'
"""

# Exécuter la requête
query_job = client.query(query)

# Récupérer les résultats de la requête
query_results = query_job.result()

# Afficher les résultats
for row in query_results:
    st.write(row)


# Curseur pour sélectionner la note moyenne
average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=4.0)

# Requête SQL pour filtrer par note moyenne
query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos` AS m
JOIN (
    SELECT movieId, AVG(rating) AS avg_rating
    FROM `caa-assignement-1-417215.Ratings.Ratings`
    GROUP BY movieId
) AS r ON m.movieId = r.movieId
WHERE r.avg_rating >= {average_rating}
"""

# Exécuter la requête
query_job = client.query(query)

# Récupérer les résultats de la requête
query_results = query_job.result()

# Afficher les résultats
for row in query_results:
    st.write(row)

# Curseur pour sélectionner l'année de sortie minimale
release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=2019)

# Requête SQL pour filtrer par année de sortie
query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE release_year >= {release_year}
"""

# Exécuter la requête
query_job = client.query(query)

# Récupérer les résultats de la requête
query_results = query_job.result()

# Afficher les résultats
for row in query_results:
    st.write(row)

