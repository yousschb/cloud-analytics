from google.cloud import bigquery
import streamlit as st

# Spécifiez le chemin vers votre fichier de clé d'API Google Cloud
key_path = "caa-assignement-1-417215-e1c1db571b4e.json"

# Créez un client BigQuery en utilisant le fichier de clé d'API
client = bigquery.Client.from_service_account_json(key_path)

# Titre de l'application
st.title("Movie Database Search")

# Organiser l'interface en deux colonnes
left_column, right_column = st.columns(2)

# Zone de recherche de titre de film
with left_column:
    search_query = st.text_input("Search for movie titles", "")

# Liste déroulante pour sélectionner le genre de film
with left_column:
    genre_choices = ["---", "Action", "Comedy", "Drama", "Horror", "Science Fiction"]
    selected_genre = st.selectbox("Select genre", genre_choices)

# Curseur pour sélectionner la note moyenne
with left_column:
    average_rating = st.slider("Select minimum average rating", min_value=0.0, max_value=5.0, step=0.1, value=4.0)

# Curseur pour sélectionner l'année de sortie minimale
with left_column:
    release_year = st.slider("Select minimum release year", min_value=1900, max_value=2022, value=2019)

# Afficher les résultats dans la colonne de droite
with right_column:
    # Construction de la requête SQL de base
    base_query = """
    SELECT title
    FROM `caa-assignement-1-417215.Movies.Infos`
    WHERE 1=1
    """

    # Ajouter les filtres en fonction des entrées de l'utilisateur
    if search_query:
        base_query += f" AND LOWER(title) LIKE LOWER('%{search_query}%')"

    if selected_genre != "---":
        base_query += f" AND LOWER(genres) LIKE LOWER('%{selected_genre}%')"

    base_query += f"""
    GROUP BY title
    HAVING AVG(rating) >= {average_rating}
    AND release_year >= {release_year}
    """

    # Exécuter la requête de filtrage
    query_results = client.query(base_query).result()

    # Afficher les résultats
    for row in query_results:
        st.write(row)
