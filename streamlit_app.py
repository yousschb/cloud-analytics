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

# Bouton de recherche
search_button = st.button("Search")

# Fonction pour récupérer les détails d'un film à partir de son tmdbId et de la langue
import requests

def get_movie_details(tmdb_id, language="en-US", api_key="VOTRE_CLE_API_TMDB"):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    params = {"language": language}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    tmdb_id = int(input("Entrez le tmdbId du film : "))
    movie_details = get_movie_details(tmdb_id)
    if movie_details:
        print("Détails du film pour tmdbId", tmdb_id, ":", movie_details)
    else:
        print("Aucun détail trouvé pour le tmdbId", tmdb_id)

if __name__ == "__main__":
    main()


# Fonction pour afficher les détails d'un film
def display_movie_details(movie):
    if movie:
        st.subheader(movie["title"])
        st.image(f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}")
        st.write("Overview:", movie["overview"])
        st.write("Release Date:", movie["release_date"])
        st.write("Genres:", ", ".join([genre["name"] for genre in movie["genres"]]))
        st.write("Cast:", ", ".join([cast["name"] for cast in movie["credits"]["cast"]]))
    else:
        st.write("No movie details found.")

# Exécuter la requête de filtrage et afficher les résultats avec les détails des films
def update_results():
    st.write("Searching for movies...")
    if search_query:
        st.write(f"Searching for movies with title containing '{search_query}'...")
        query = f"""
            SELECT m.tmdbId, m.language
            FROM `caa-assignement-1-417215.Movies.Infos` AS m
            WHERE LOWER(m.title) LIKE LOWER('%{search_query}%')
        """
        st.write("Executing query:", query)
        query_job = client.query(query)
        results = query_job.result()
        if results.total_rows == 0:
            st.write("No movies found matching the search criteria.")
        else:
            st.write("Movies found! Displaying details...")
            for row in results:
                tmdb_id = row["tmdbId"]
                language = row["language"]
                st.write(f"Fetching details for movie with tmdbId '{tmdb_id}'...")
                movie_details = get_movie_details(tmdb_id, language)
                st.write("Movie details:", movie_details)
                display_movie_details(movie_details)

# Appel à la fonction update_results pour afficher les résultats dans l'interface utilisateur
if search_button:
    update_results()


