import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

from config import settings

API_KEY = os.getenv("TMDB_API_KEY")




def _get(url: str, params: dict = None):
    params = params or {}
    params["api_key"] = API_KEY
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    return r.json()


def fetch_popular(pages: int = None) -> list[dict]:
    pages = pages or settings.TMDB_PAGES
    movies = []
    for p in range(1, pages + 1):
        data = _get(f"{settings.TMDB_BASE_URL}/movie/popular", {"page": p})
        if data:
            movies.extend(data["results"])
        time.sleep(0.2)
    return movies


def fetch_full(movie_id: int) -> dict:
    movie    = _get(f"{settings.TMDB_BASE_URL}/movie/{movie_id}");       time.sleep(0.1)
    credits  = _get(f"{settings.TMDB_BASE_URL}/movie/{movie_id}/credits"); time.sleep(0.1)
    keywords = _get(f"{settings.TMDB_BASE_URL}/movie/{movie_id}/keywords"); time.sleep(0.1)
    return {"movie": movie, "credits": credits, "keywords": keywords}



def run(pages: int = 1, out_dir: str = None) -> list[dict]:
    out_dir = out_dir or settings.TMDB_DATA_DIR
    os.makedirs(out_dir, exist_ok=True)

    movies  = fetch_popular(pages)
    dataset = []

    for m in movies:
        full = fetch_full(m["id"])
        if full["movie"]:
            dataset.append(full)
            fpath = os.path.join(out_dir, f"{m['id']}.json")
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(full, f, indent=2)

    all_path = os.path.join(out_dir, "all.json")
    with open(all_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"[fetch_tmdb] Done — {len(dataset)} movies saved to '{out_dir}'")
    return dataset


if __name__ == "__main__":
    run()
