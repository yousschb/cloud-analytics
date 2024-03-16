import requests
import streamlit as st

# Clé API TMDb
TMDB_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMWNmMjQ2MDE5MDkyZTY0ZDI1YWU1ZTNmMjVhMzkzMyIsInN1YiI6IjY1ZjU5ZTRlMDZmOTg0MDE3Y2M3Yzg3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zF_TJxsIBuU9yHRlEQWEYYF7ZZg9ZoibgSnndHDhabA"

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
    st.title("Movie Details")
    tmdb_id = st.text_input("Enter the tmdbId of the movie:")
    if st.button("Get Movie Details") and tmdb_id:  # Ajoutez un bouton pour déclencher la recherche
        movie_details = get_movie_details(tmdb_id)
        if movie_details:
            st.write("### Movie Details:")
            st.write(movie_details)
        else:
            st.write("No movie details found for the provided tmdbId.")

if __name__ == "__main__":
    main()
