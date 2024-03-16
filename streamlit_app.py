from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Titre de l'application
st.title("Movie Database Search")

# Afficher le champ de recherche pour les titres de films
search_query = st.text_input("Search for movie titles", "")

# Requête SQL pour l'autocomplétion des titres de films
autocomplete_query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos`
WHERE LOWER(title) LIKE LOWER('%{search_query}%')
"""

# Exécuter la requête d'autocomplétion
autocomplete_results = client.query(autocomplete_query).result()

# Afficher les résultats d'autocomplétion
autocomplete_titles = [row["title"] for row in autocomplete_results]
st.write("Autocomplete suggestions:", autocomplete_titles)

# Liste déroulante pour sélectionner la langue
language = st.selectbox("Select language", ["English", "French", "German", "Spanish", "Italian"])

# Liste déroulante pour sélectionner le genre de film
genre = st.selectbox("Select genre", ["Action", "Comedy", "Drama", "Horror", "Science Fiction"])

# Curseur pour sélectionner la note moyenne
average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=4.0)

# Curseur pour sélectionner l'année de sortie minimale
release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=2019)

# Requête SQL principale pour filtrer les films
main_query = f"""
SELECT title
FROM `caa-assignement-1-417215.Movies.Infos` AS m
JOIN (
    SELECT movieId, AVG(rating) AS avg_rating
    FROM `caa-assignement-1-417215.Ratings.Ratings`
    GROUP BY movieId
) AS r ON m.movieId = r.movieId
WHERE LOWER(m.title) LIKE LOWER('%{search_query}%')
    AND m.language = '{language}'
    AND genres LIKE '%{genre}%'
    AND r.avg_rating >= {average_rating}
    AND m.release_year >= {release_year}
"""

# Exécuter la requête principale
main_results = client.query(main_query).result()

# Afficher les résultats principaux
for row in main_results:
    st.write(row)
