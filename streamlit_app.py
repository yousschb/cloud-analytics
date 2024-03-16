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
    tmdb_id = input("Entrez le tmdbId du film : ")
    movie_details = get_movie_details(tmdb_id)
    if movie_details:
        print("Détails du film pour tmdbId", tmdb_id, ":", movie_details)
    else:
        print("Aucun détail trouvé pour le tmdbId", tmdb_id)

if __name__ == "__main__":
    main()
