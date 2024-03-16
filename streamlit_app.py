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

    if movie_name:  # Vérifie si l'utilisateur a entré des mots-clés avant de lancer la recherche
        # Recherche de tous les résultats de nom de film contenant les mots clés
        query = f"""
            SELECT title
            FROM `caa-assignement-1-417215.Movies.Infos`
            WHERE LOWER(title) LIKE LOWER('%{movie_name}%')
        """
        query_job = client.query(query)
        results = query_job.result()

        movie_options = [row.title for row in results]

        if not movie_options:
            st.write("No movie found matching the provided keywords.")
        else:
            st.write("Select a movie to view details:")
            selected_movie = st.selectbox("Movie titles", movie_options)
            if selected_movie:
                # Recherche du tmdb_id correspondant au nom du film sélectionné
                query = f"""
                    SELECT tmdbId
                    FROM `caa-assignement-1-417215.Movies.Infos`
                    WHERE LOWER(title) = LOWER('{selected_movie}')
                    LIMIT 1
                """
                query_job = client.query(query)
                results = query_job.result()
                for row in results:
                    tmdb_id = row.tmdbId
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
                    st.write("No movie found with the provided name.")

    # Ajout des options supplémentaires
    st.write("Additional Options:")
    
    # Filter by language (SQL)
    language = st.text_input("Filter by language (SQL):")
    if language:
        query = f"""
            SELECT title
            FROM `caa-assignement-1-417215.Movies.Infos`
            WHERE LOWER(language) LIKE LOWER('%{language}%')
        """
        query_job = client.query(query)
        results = query_job.result()
        movie_options = [row.title for row in results]
        st.write("Movies in the selected language:")
        for movie in movie_options:
            st.write(movie)

    # Filter by movie genre (SQL)
    genre = st.text_input("Filter by movie genre (SQL):")
    if genre:
        query = f"""
            SELECT title
            FROM `caa-assignement-1-417215.Movies.Infos`
            WHERE LOWER(genre) LIKE LOWER('%{genre}%')
        """
        query_job = client.query(query)
        results = query_job.result()
        movie_options = [row.title for row in results]
        st.write("Movies in the selected genre:")
        for movie in movie_options:
            st.write(movie)

    # Filter by average rating of a movie (SQL)
    rating = st.text_input("Filter by average rating of a movie (SQL):")
    if rating:
        query = f"""
            SELECT title
            FROM `caa-assignement-1-417215.Movies.Infos`
            WHERE rating > {rating}
        """
        query_job = client.query(query)
        results = query_job.result()
        movie_options = [row.title for row in results]
        st.write("Movies with average rating higher than the provided value:")
        for movie in movie_options:
            st.write(movie)

    # Filter by release year (e.g., after 2019)
    release_year = st.text_input("Filter by release year (e.g., after 2019):")
    if release_year:
        query = f"""
            SELECT title
            FROM `caa-assignement-1-417215.Movies.Infos`
            WHERE EXTRACT(YEAR FROM release_date) > {release_year}
        """
        query_job = client.query(query)
        results = query_job.result()
        movie_options = [row.title for row in results]
        st.write("Movies released after the provided year:")
        for movie in movie_options:
            st.write(movie)

if __name__ == "__main__":
    main()
