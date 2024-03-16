from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Titre de l'application
st.title("Movie Database Search")

# Zone de recherche de titre de film
search_query = st.text_input("Search for movie titles", "")

# Liste déroulante pour sélectionner le genre de film
genre_choices = ["---", "Action", "Comedy", "Drama", "Horror", "Science Fiction"]
selected_genre = st.selectbox("Select genre", genre_choices)

# Curseur pour sélectionner la note moyenne
average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=3.0)

# Curseur pour sélectionner l'année de sortie minimale
release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=1980)

# Construction de la requête SQL de base
base_query = """
SELECT m.title
FROM `caa-assignement-1-417215.Movies.Infos` AS m
JOIN (
    SELECT movieId, AVG(rating) AS avg_rating
    FROM `caa-assignement-1-417215.Movies.ratings`
    GROUP BY movieId
) AS r ON m.movieId = r.movieId
"""

# Ajouter les filtres en fonction des entrées de l'utilisateur
if search_query or selected_genre != "---" or average_rating != 3.0 or release_year != 1980:
    base_query += " WHERE 1=1"  # Début de la clause WHERE uniquement si des critères sont spécifiés
    
    if search_query:
        base_query += " AND LOWER(m.title) LIKE LOWER(@search_query)"
    if selected_genre != "---":
        base_query += " AND LOWER(m.genres) LIKE LOWER(@selected_genre)"
    base_query += " AND r.avg_rating >= @average_rating AND m.release_year >= @release_year"

    # Préparer les paramètres de requête
    query_params = {
        "search_query": f"%{search_query}%" if search_query else None,
        "selected_genre": f"%{selected_genre}%" if selected_genre != "---" else None,
        "average_rating": average_rating,
        "release_year": release_year
    }

    # Exécuter la requête de filtrage avec les paramètres
    query_job = client.query(base_query, query_params=query_params)

    # Afficher les résultats
    results = query_job.result()
    if results.total_rows == 0:
        st.write("No movies found matching the criteria.")
    else:
        for row in results:
            st.write(row)
else:
    st.write("Please provide search criteria.")
