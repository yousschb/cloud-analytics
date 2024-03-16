from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Titre de l'application
st.title("Movie Database Search")

# Afficher le champ de recherche pour les titres de films
search_query = st.text_input("Search for movie titles", "")

# Vérifier si la barre de recherche n'est pas vide
if search_query:
    # Requête SQL pour l'autocomplétion des titres de films
    autocomplete_query = f"""
    SELECT title
    FROM `caa-assignement-1-417215.Movies.Infos`
    WHERE LOWER(title) LIKE LOWER('%{search_query}%')
    """

    # Exécuter la requête d'autocomplétion
    autocomplete_results = client.query(autocomplete_query).result()

    # Afficher les résultats de l'autocomplétion
    for row in autocomplete_results:
        st.write(row)

# Liste déroulante pour sélectionner la langue
language = st.selectbox("Select language", ["English", "French", "German", "Spanish", "Italian"])

# Vérifier si la langue est sélectionnée
if language:
    # Requête SQL pour filtrer par langue
    language_query = f"""
    SELECT title
    FROM `caa-assignement-1-417215.Movies.Infos`
    WHERE language = '{language}'
    """

    # Exécuter la requête de filtrage par langue
    language_results = client.query(language_query).result()

    # Afficher les résultats du filtrage par langue
    for row in language_results:
        st.write(row)

# Liste déroulante pour sélectionner le genre de film
genre = st.selectbox("Select genre", ["Action", "Comedy", "Drama", "Horror", "Science Fiction"])

# Vérifier si le genre est sélectionné
if genre:
    # Requête SQL pour filtrer par genre de film
    genre_query = f"""
    SELECT title
    FROM `caa-assignement-1-417215.Movies.Infos`
    WHERE genres LIKE '%{genre}%'
    """

    # Exécuter la requête de filtrage par genre de film
    genre_results = client.query(genre_query).result()

    # Afficher les résultats du filtrage par genre de film
    for row in genre_results:
        st.write(row)

# Curseur pour sélectionner la note moyenne
average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=4.0)

# Vérifier si la note moyenne est sélectionnée
if average_rating:
    # Requête SQL pour filtrer par note moyenne
    rating_query = f"""
    SELECT m.title
    FROM `caa-assignement-1-417215.Movies.Infos` AS m
    JOIN (
        SELECT movieId, AVG(rating) AS avg_rating
        FROM `caa-assignement-1-417215.Ratings.Ratings`
        GROUP BY movieId
    ) AS r ON m.movieId = r.movieId
    WHERE r.avg_rating >= {average_rating}
    """

    # Exécuter la requête de filtrage par note moyenne
    rating_results = client.query(rating_query).result()

    # Afficher les résultats du filtrage par note moyenne
    for row in rating_results:
        st.write(row)

# Curseur pour sélectionner l'année de sortie minimale
release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=2019)

# Vérifier si l'année de sortie minimale est sélectionnée
if release_year:
    # Requête SQL pour filtrer par année de sortie
    year_query = f"""
    SELECT title
    FROM `caa-assignement-1-417215.Movies.Infos`
    WHERE release_year >= {release_year}
    """

    # Exécuter la requête de filtrage par année de sortie
    year_results = client.query(year_query).result()

    # Afficher les résultats du filtrage par année de sortie
    for row in year_results:
        st.write(row)
