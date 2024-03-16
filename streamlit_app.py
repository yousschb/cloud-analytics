from google.cloud import bigquery
import streamlit as st
import requests

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



# Clé API TMDb
TMDB_API_KEY = "c1cf246019092e64d25ae5e3f25a3933"

# Fonction pour obtenir les détails du film à partir de l'API TMDb
def get_movie_details(title):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['total_results'] > 0:
            movie_id = data['results'][0]['id']
            movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            params = {
                "api_key": TMDB_API_KEY
            }
            movie_response = requests.get(movie_details_url, params=params)
            if movie_response.status_code == 200:
                movie_data = movie_response.json()
                return movie_data
            else:
                return "Failed to fetch movie details"
        else:
            return "Movie not found"
    else:
        return "Failed to fetch movie details"




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
                    movie_details = get_movie_details(movie_title)
                    st.write(movie_details)
