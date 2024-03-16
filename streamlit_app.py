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
    movie_keywords = st.text_input("Enter keywords for movie search:")
    if movie_keywords:
        # Recherche de films correspondant aux mots-clés dans la table Movies.Infos
        query = f"""
            SELECT title
            FROM `caa-assignement-1-417215.Movies.Infos`
            WHERE LOWER(title) LIKE LOWER('%{movie_keywords}%')
            LIMIT 10
        """
        query_job = client.query(query)
        results = query_job.result()

        if results.total_rows > 0:
            st.write("### Search Results:")
            for row in results:
                movie_title = row.title
                if st.button(movie_title):
                    # Recherche du tmdb_id du film sélectionné
                    tmdb_id_query = f"""
                        SELECT tmdbId
                        FROM `caa-assignement-1-417215.Movies.Infos`
                        WHERE LOWER(title) = LOWER('{movie_title}')
                        LIMIT 1
                    """
                    tmdb_id_query_job = client.query(tmdb_id_query)
                    tmdb_id_results = tmdb_id_query_job.result()
                    for tmdb_id_row in tmdb_id_results:
                        tmdb_id = tmdb_id_row.tmdbId
                        break

                    if tmdb_id:
                        movie_details = get_movie_details(tmdb_id)
                        if movie_details:
                            col1, col2 = st.columns([1, 2])  # Diviser la page en 2 colonnes

                            # Afficher l'affiche du film dans la première colonne
                            if movie_details['poster_path']:
                                col1.image(f"https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}", caption="Movie Poster", use_column_width=True)

                            # Afficher les informations du film dans la deuxième colonne
                            col2.write(f"Title: {movie_details['title']}")
                            col2.write(f"Overview: {movie_details['overview']}")
                            col2.write(f"Release Date: {movie_details['release_date']}")
                            col2.write(f"Genres: {', '.join(genre['name'] for genre in movie_details['genres'])}")
                            col2.write(f"Average Vote: {movie_details['vote_average']}")
                        else:
                            st.write("No movie details found for the provided tmdbId.")
                    else:
                        st.write("No movie found with the provided title.")
        else:
            st.write("No movies found matching the provided keywords.")

if __name__ == "__main__":
    main()
