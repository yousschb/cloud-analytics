import requests
from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Clé API TMDb
TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMWNmMjQ2MDE5MDkyZTY0ZDI1YWU1ZTNmMjVhMzkzMyIsInN1YiI6IjY1ZjU5ZTRlMDZmOTg0MDE3Y2M3Yzg3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zF_TJxsIBuU9yHRlEQWEYYF7ZZg9ZoibgSnndHDhabA"

# Créez un client BigQuery en utilisant le fichier de clé d'API Google Cloud
client = bigquery.Client.from_service_account_json(key_path)

# Fonction pour obtenir les détails du film à partir du TMDb
def get_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    movie_name = st.text_input("Enter keywords of the movie name:")
    
    if st.button("Search"):
        if movie_name:  # Vérifie si l'utilisateur a entré des mots-clés avant de lancer la recherche
            # Recherche de tous les résultats de nom de film contenant les mots clés
            query = f"""
                SELECT m.title, m.tmdbId
                FROM `caa-assignement-1-417215.Movies.Infos` AS m
                WHERE LOWER(m.title) LIKE LOWER('%{movie_name}%')
            """
            query_job = client.query(query)
            results = query_job.result()

            if results.total_rows == 0:
                st.write("No movie found matching the provided keywords.")
            else:
                st.write("### Results:")
                for row in results:
                    movie_title = row.title
                    tmdb_id = row.tmdbId
                    if st.button(movie_title):  # Bouton pour chaque titre de film
                        movie_details = get_movie_details(tmdb_id)
                        if movie_details:
                            st.image(f"https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}", caption="Movie Poster")
                            st.write(f"Title: {movie_details['title']}")
                            st.write(f"Overview: {movie_details['overview']}")
                            st.write(f"Release Date: {movie_details['release_date']}")
                            st.write(f"Genres: {', '.join(genre['name'] for genre in movie_details['genres'])}")
                            st.write(f"Average Vote: {movie_details['vote_average']}")
                        else:
                            st.write("No movie details found for the provided tmdbId.")

if __name__ == "__main__":
    main()
