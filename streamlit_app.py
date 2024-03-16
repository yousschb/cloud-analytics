from google.cloud import bigquery
import streamlit as st
from tmdbv3api import TMDb
from tmdbv3api import Movie

# Clé API TMDb
TMDB_API_KEY = "c1cf246019092e64d25ae5e3f25a3933"

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Initialisez l'objet TMDb avec votre jeton d'accès en lecture
tmdb = TMDb()
tmdb.api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMWNmMjQ2MDE5MDkyZTY0ZDI1YWU1ZTNmMjVhMzkzMyIsInN1YiI6IjY1ZjU5ZTRlMDZmOTg0MDE3Y2M3Yzg3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zF_TJxsIBuU9yHRlEQWEYYF7ZZg9ZoibgSnndHDhabA'

# Initialisez l'objet Movie pour effectuer des requêtes sur les films
movie = Movie()

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
def build_query():
    base_query = """
    SELECT m.title, AVG(r.rating) as avg_rating
    FROM `caa-assignement-1-417215.Movies.Infos` AS m
    JOIN `caa-assignement-1-417215.Movies.ratings` AS r ON m.movieId = r.movieId
    WHERE 1=1
    """
    # Ajouter les filtres en fonction des entrées de l'utilisateur
    filters = []
    if search_query:
        filters.append(f"LOWER(m.title) LIKE LOWER('%{search_query}%')")
    if selected_genre != "---":
        filters.append(f"LOWER(m.genres) LIKE LOWER('%{selected_genre}%')")
    filters.append(f"m.release_year >= {release_year}")
    
    if filters:
        base_query += " AND " + " AND ".join(filters)
    
    base_query += f" GROUP BY m.title HAVING AVG(r.rating) >= {average_rating}"  # Utilisation de f-string pour insérer la variable
    
    return base_query


# Exécuter la requête de filtrage et afficher les résultats
def update_results():
    query = build_query()
    if query.strip() == "":
        return "Please provide search criteria."
    else:
        query_job = client.query(query)
        results = query_job.result()
        if results.total_rows == 0:
            return "No movies found matching the criteria."
        else:
            return results

# Importation de la bibliothèque d'icônes
from streamlit.components.v1 import html

# Fonction pour générer des étoiles en fonction de la note
def generate_stars(avg_rating):
    if avg_rating is None:  # Vérification si la note est nulle
        return "No rating available"
    
    filled_stars = int(avg_rating)
    half_star = avg_rating - filled_stars >= 0.5
    empty_stars = 5 - filled_stars - (1 if half_star else 0)
    
    stars_html = ""
    for _ in range(filled_stars):
        stars_html += "★ "
    if half_star:
        stars_html += "☆ "
    for _ in range(empty_stars):
        stars_html += "☆ "
    
    return stars_html



# Afficher les résultats de la recherche
if st.button("Search"):
    results = update_results()
    if isinstance(results, str):
        st.write(results)
    else:
        st.write("### Results:")
        for row in results:
            movie_title = row[0]
            avg_rating = row[1]
            if st.button(movie_title):
                # Afficher les détails du film sélectionné dans un panneau déroulant
                with st.expander(f"Details of {movie_title}"):
                    search_result = movie.search(movie_title)
                    if search_result:
                        movie_details = movie.details(search_result[0].id)
                        st.write(movie_details)
