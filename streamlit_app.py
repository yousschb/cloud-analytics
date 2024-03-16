import requests
from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Clé API TMDb
TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMWNmMjQ2MDE5MDkyZTY0ZDI1YWU1ZTNmMjVhMzkzMyIsInN1YiI6IjY1ZjU5ZTRlMDZmOTg0MDE3Y2M3Yzg3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zF_TJxsIBuU9yHRlEQWEYYF7ZZg9ZoibgSnndHDhabA"

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

# Fonction pour obtenir les détails du film à partir de l'API TMDb
# Fonction pour obtenir les films populaires du jour à partir de l'API TMDb
def get_trending_movies():
    base_url = "https://api.themoviedb.org/3/trending/all/day"
    params = {
        "api_key": TMDB_API_KEY
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        return "Failed to fetch trending movies"

# Afficher les résultats des films populaires du jour
trending_movies = get_trending_movies()
if isinstance(trending_movies, str):
    st.write(trending_movies)
else:
    st.write("### Trending Movies Today:")
    for movie in trending_movies:
        st.write(f"- {movie['title']} ({movie['release_date']})")

