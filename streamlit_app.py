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
    tmdb_id = st.text_input("Enter the tmdbId of the movie:")
    if st.button("Get Movie Details") and tmdb_id:  # Ajoutez un bouton pour déclencher la recherche
        movie_details = get_movie_details(tmdb_id)
        if movie_details:
            st.write("### Movie Details:")
            st.write(f"Title: {movie_details['title']}")
            st.write(f"Overview: {movie_details['overview']}")
            st.write(f"Release Date: {movie_details['release_date']}")
            st.write(f"Budget: ${movie_details['budget']}")
            st.write(f"Genres: {', '.join(genre['name'] for genre in movie_details['genres'])}")
            st.write(f"Popularity: {movie_details['popularity']}")
            st.write(f"Average Vote: {movie_details['vote_average']}")
            st.write(f"Vote Count: {movie_details['vote_count']}")
        else:
            st.write("No movie details found for the provided tmdbId.")

if __name__ == "__main__":
    main()
