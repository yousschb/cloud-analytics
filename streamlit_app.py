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

# Requête de filtrage et affichage des résultats
def update_results(movie_name, selected_genre, average_rating, release_year):
    query = build_query(movie_name, selected_genre, average_rating, release_year)
    if query.strip() == "":
        return "Please provide search criteria."
    else:
        query_job = client.query(query)
        results = query_job.result()
        if results.total_rows == 0:
            return "No movies found matching the criteria."
        else:
            return results

# Construction de la requête SQL de base
def build_query(movie_name, selected_genre, average_rating, release_year):
    base_query = """
    SELECT m.title, AVG(r.rating) as avg_rating
    FROM `caa-assignement-1-417215.Movies.Infos` AS m
    JOIN `caa-assignement-1-417215.Movies.ratings` AS r ON m.movieId = r.movieId
    WHERE 1=1
    """
    # Ajouter les filtres en fonction des entrées de l'utilisateur
    filters = []
    if movie_name:
        filters.append(f"LOWER(m.title) LIKE LOWER('%{movie_name}%')")
    if selected_genre != "---":
        filters.append(f"LOWER(m.genres) LIKE LOWER('%{selected_genre}%')")
    filters.append(f"m.release_year >= {release_year}")
    
    if filters:
        base_query += " AND " + " AND ".join(filters)
    
    base_query += f" GROUP BY m.title HAVING AVG(r.rating) >= {average_rating}"  # Utilisation de f-string pour insérer la variable
    
    return base_query

def main():
    # Zone de recherche de titre de film
    movie_name = st.text_input("Enter keywords of the movie name:")

    # Liste déroulante pour sélectionner le genre de film
    genre_choices = ["---", "Action", "Comedy", "Drama", "Horror", "Science Fiction"]
    selected_genre = st.selectbox("Select genre", genre_choices)

    # Curseur pour sélectionner la note moyenne
    average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=3.0)

    # Curseur pour sélectionner l'année de sortie minimale
    release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=1980)

    # Bouton pour mettre à jour les résultats
    if st.button("Search"):
        results = update_results(movie_name, selected_genre, average_rating, release_year)
        if isinstance(results, str):
            st.write(results)
        else:
            st.write("### Results:")
            for row in results:
                movie_title = row[0]
                avg_rating = row[1]
                st.write(f"- {movie_title} - Average Rating: {generate_stars(avg_rating)}")

    if 'results' in locals():  # Vérifie si la variable results existe
        movie_options = [str(row.title) for row in results]

        if not movie_options:
            st.write("No movie found matching the provided keywords.")
        else:
            st.write("Select a movie to view details:")
            for index, selected_movie in enumerate(movie_options):
                if st.button(selected_movie, key=f"button_{index}"):  # Utilisation de l'index pour créer une clé unique
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

if __name__ == "__main__":
    main()
