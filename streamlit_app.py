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
    # Zone de recherche de titre de film
    movie_name = st.text_input("Enter keywords of the movie name:")

    # Liste déroulante pour sélectionner le genre de film
    genre_choices = ["---", "Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    selected_genre = st.selectbox("Select genre", genre_choices)

    # Curseur pour sélectionner la note moyenne
    average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=3.0)

    # Curseur pour sélectionner l'année de sortie minimale
    release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=1980)

    # Variable de contrôle pour déterminer si les critères de recherche ont été sélectionnés
    criteria_selected = movie_name or selected_genre != "---" or average_rating != 3.0 or release_year != 1980

    # Requête de filtrage et affichage des résultats si les critères sont sélectionnés
    if criteria_selected:
        query = build_query(movie_name, selected_genre, average_rating, release_year)
        if query.strip() == "":
            st.write("Please provide search criteria.")
        else:
            query_job = client.query(query)
            results = query_job.result()
            if results.total_rows == 0:
                st.write("No movies found matching the criteria.")
            else:
                st.write("### Results:")
                for row in results:
                    movie_title = row[0]
                    avg_rating = row[1]
                    button_clicked = st.button(movie_title)
                    if button_clicked:
                       # Nettoyer le titre du film en enlevant les caractères spéciaux
                        clean_movie_title = ''.join(e for e in movie_title if e.isalnum() or e.isspace()).strip()
                        
                        # Recherche du tmdb_id correspondant au nom du film sélectionné (après nettoyage)
                        query_tmdb_id = f"""
                            SELECT tmdbId, title
                            FROM `caa-assignement-1-417215.Movies.Infos`
                        """
                        query_job_tmdb_id = client.query(query_tmdb_id)
                        results_tmdb_id = query_job_tmdb_id.result()
                        
                        # Récupération du tmdbId s'il existe
                        tmdb_id = None
                        for row_tmdb_id in results_tmdb_id:
                            if clean_movie_title.lower() == ''.join(e for e in row_tmdb_id.title if e.isalnum() or e.isspace()).strip().lower():
                                tmdb_id = row_tmdb_id.tmdbId
                                break



                        if tmdb_id:
                            movie_details = get_movie_details(tmdb_id)
                            if movie_details:
                                col1, col2 = st.columns([1, 3])  # Diviser la page en 2 colonnes

                                # Afficher l'affiche du film dans la première colonne
                                if movie_details['poster_path']:
                                    col1.image(f"https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}")

                                # Afficher les informations du film dans la deuxième colonne
                                col2.write(f"**Title:** {movie_details['title']}")
                                col2.write(f"**Overview:** {movie_details['overview']}")
                                col2.write(f"**Release Date:** {movie_details['release_date']}")
                                col2.write(f"**Genres:** {', '.join(genre['name'] for genre in movie_details['genres'])}")
                                col2.write(f"**Average Rating:** {generate_stars(avg_rating)}")
                            else:
                                st.write("No movie details found for the provided tmdbId.")
                        else:
                            st.write("No movie found with the provided name.")

# Fonction pour construire la requête SQL en fonction des critères de recherche
def build_query(movie_name, selected_genre, average_rating, release_year):
    base_query = """
        SELECT m.title, AVG(r.rating) as avg_rating
        FROM `caa-assignement-1-417215.Movies.Infos` AS m
        JOIN `caa-assignement-1-417215.Movies.ratings` AS r ON m.movieId = r.movieId
        WHERE 1=1
        """
    # Ajouter les filtres en fonction des entrées de l'utilisateur
    filters = []
    
    # Recherche du tmdb_id correspondant au nom du film sélectionné (après nettoyage)
    if movie_name:    
        # Construire la condition de recherche pour chaque bloc de mot-clé
        keyword_conditions = []
        for keyword in movie_name.split():
            keyword_conditions.append(f"LOWER(m.title) LIKE LOWER('{keyword}')")
        
        # Ajouter les conditions avec un AND pour rechercher les titres contenant tous les blocs de mots-clés
        if len(keyword_conditions) > 1:  # S'assurer qu'il y a plus d'un mot-clé
            filters.append("(" + " AND ".join(keyword_conditions) + ")")
        else:
            # Si un seul mot-clé est fourni, ne pas ajouter de filtre supplémentaire
            filters.append(keyword_conditions[0])



        
    if selected_genre != "---":
    # Si le genre sélectionné contient une barre verticale, on considère chacun des genres séparément
        if "|" in selected_genre:
            selected_genres = selected_genre.split("|")
            genre_filters = [f"'{genre}' IN UNNEST(SPLIT(m.genres, '|'))" for genre in selected_genres]
            filters.append("(" + " OR ".join(genre_filters) + ")")
        else:
            # Si le genre sélectionné ne contient pas de barre verticale, on peut simplement le rechercher dans la colonne genres
            filters.append(f"'{selected_genre}' IN UNNEST(SPLIT(m.genres, '|'))")


    filters.append(f"m.release_year >= {release_year}")
    
    if filters:
        base_query += " AND " + " AND ".join(filters)
    
    base_query += " GROUP BY m.title"  # Ne pas ajouter la clause HAVING pour le moment
    
    return base_query


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

if __name__ == "__main__":
    main()
