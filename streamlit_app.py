from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Titre de l'application
st.title("Movie Database Search")

# Zone de recherche de titre de film avec un widget clé
search_query = st.text_input("Search for movie titles", key="search_query")

# Liste déroulante pour sélectionner le genre de film avec un widget clé
genre_choices = ["---", "Action", "Comedy", "Drama", "Horror", "Science Fiction"]
selected_genre = st.selectbox("Select genre", genre_choices, key="selected_genre")

# Curseur pour sélectionner la note moyenne avec un widget clé
average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=3.0, key="average_rating")

# Curseur pour sélectionner l'année de sortie minimale avec un widget clé
release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=1980, key="release_year")

# Construction de la requête SQL de base
def build_query():
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
    filters = []
    if search_query:
        filters.append(f"LOWER(m.title) LIKE LOWER('%{search_query}%')")
    if selected_genre != "---":
        filters.append(f"LOWER(m.genres) LIKE LOWER('%{selected_genre}%')")
    filters.append(f"r.avg_rating >= {average_rating}")
    filters.append(f"m.release_year >= {release_year}")
    
    if filters:
        base_query += " WHERE " + " AND ".join(filters)
    
    return base_query

# Exécuter la requête de filtrage et afficher les résultats
def run_query():
    query = build_query()
    if query.strip() == "":
        st.write("Please provide search criteria.")
    else:
        query_job = client.query(query)
        results = query_job.result()
        if results.total_rows == 0:
            st.write("No movies found matching the criteria.")
        else:
            for row in results:
                st.write(row)

# Appel de la fonction pour exécuter la requête et afficher les résultats
run_query()
