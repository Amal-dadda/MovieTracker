import requests

TMDB_API_KEY = "8837833c44b4352bb2ee6b5f5662a714"

def search_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    return []

def get_trending_movies(time_window="week"):
    url = f"https://api.themoviedb.org/3/trending/movie/{time_window}"
    resp = requests.get(url, params={"api_key": TMDB_API_KEY})
    if resp.status_code == 200:
        return resp.json().get("results", [])
    return []