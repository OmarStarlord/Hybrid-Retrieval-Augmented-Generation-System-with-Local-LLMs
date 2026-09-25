import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from vector.chroma_index import index_folder, get_collection
from ingestion.fetch_tmdb import run as fetch_tmdb_data
from graph.neo4j_client import run_cypher, close_driver


BATCH_SIZE = 100


def setup_neo4j_schema():
    print("[build_graph] Setting up Neo4j schema...", flush=True)

    # Prefer tmdb_id over movie name because different movies can share the same title.
    run_cypher("""
    CREATE CONSTRAINT movie_tmdb_id IF NOT EXISTS
    FOR (m:Movie) REQUIRE m.tmdb_id IS UNIQUE
    """)

    run_cypher("""
    CREATE CONSTRAINT person_name IF NOT EXISTS
    FOR (p:Person) REQUIRE p.name IS UNIQUE
    """)

    run_cypher("""
    CREATE CONSTRAINT genre_name IF NOT EXISTS
    FOR (g:Genre) REQUIRE g.name IS UNIQUE
    """)

    run_cypher("""
    CREATE CONSTRAINT keyword_name IF NOT EXISTS
    FOR (k:Keyword) REQUIRE k.name IS UNIQUE
    """)

    # Helpful for title lookups.
    try:
        run_cypher("""
        CREATE INDEX movie_name IF NOT EXISTS
        FOR (m:Movie) ON (m.name)
        """)
    except Exception as e:
        print(f"[build_graph] Movie name index warning: {e}", flush=True)

    # Helpful for text search over plots.
    try:
        run_cypher("""
        CREATE FULLTEXT INDEX movie_plot IF NOT EXISTS
        FOR (m:Movie) ON EACH [m.plot]
        """)
    except Exception as e:
        print(f"[build_graph] Fulltext index warning: {e}", flush=True)

    print("[build_graph] Neo4j schema setup complete.", flush=True)


def load_tmdb_dataset(data_dir: str) -> list[dict]:
    all_path = os.path.join(data_dir, "all.json")

    if not os.path.exists(all_path):
        raise FileNotFoundError(f"Could not find TMDB dataset at: {all_path}")

    with open(all_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"[build_graph] Loaded {len(dataset)} movies from {all_path}", flush=True)
    return dataset


def normalize_movie_item(item: dict) -> dict | None:
    movie = item.get("movie") or {}
    credits = item.get("credits") or {}
    keywords_obj = item.get("keywords") or {}

    movie_id = movie.get("id")
    title = movie.get("title") or movie.get("name")

    if not movie_id or not title:
        return None

    genres = [
        genre.get("name")
        for genre in movie.get("genres") or []
        if genre.get("name")
    ]

    cast = [
        {
            "name": actor.get("name"),
            "character": actor.get("character") or "",
            "order": actor.get("order"),
        }
        for actor in (credits.get("cast") or [])[:10]
        if actor.get("name")
    ]

    directors = [
        person.get("name")
        for person in credits.get("crew") or []
        if person.get("job") == "Director" and person.get("name")
    ]

    keywords_raw = keywords_obj.get("keywords") or keywords_obj.get("results") or []
    keywords = [
        keyword.get("name")
        for keyword in keywords_raw
        if keyword.get("name")
    ]

    return {
        "tmdb_id": int(movie_id),
        "name": title,
        "plot": movie.get("overview") or "",
        "release_date": movie.get("release_date") or "",
        "vote_average": movie.get("vote_average"),
        "popularity": movie.get("popularity"),
        "genres": genres,
        "cast": cast,
        "directors": directors,
        "keywords": keywords,
    }


def insert_movie_batch(movies: list[dict]):
    if not movies:
        return

    run_cypher(
        """
        UNWIND $movies AS movie

        MERGE (m:Movie {tmdb_id: movie.tmdb_id})
        SET m.name = movie.name,
            m.plot = movie.plot,
            m.release_date = movie.release_date,
            m.vote_average = movie.vote_average,
            m.popularity = movie.popularity

        WITH m, movie

        FOREACH (genre_name IN movie.genres |
            MERGE (g:Genre {name: genre_name})
            MERGE (m)-[:HAS_GENRE]->(g)
        )

        FOREACH (actor IN movie.cast |
            MERGE (p:Person {name: actor.name})
            MERGE (p)-[r:ACTED_IN]->(m)
            SET r.character = actor.character,
                r.order = actor.order
        )

        FOREACH (director_name IN movie.directors |
            MERGE (p:Person {name: director_name})
            MERGE (p)-[:DIRECTED]->(m)
        )

        FOREACH (keyword_name IN movie.keywords |
            MERGE (k:Keyword {name: keyword_name})
            MERGE (m)-[:HAS_KEYWORD]->(k)
        )
        """,
        {"movies": movies},
    )


def build_and_insert_graph(data_dir: str):
    print("[build_graph] Building and inserting Neo4j graph...", flush=True)

    dataset = load_tmdb_dataset(data_dir)

    movies = []
    skipped = 0

    for item in dataset:
        normalized = normalize_movie_item(item)

        if normalized is None:
            skipped += 1
            continue

        movies.append(normalized)

    print(
        f"[build_graph] Prepared {len(movies)} movies for insertion. Skipped {skipped}.",
        flush=True,
    )

    inserted = 0

    for start in range(0, len(movies), BATCH_SIZE):
        batch = movies[start:start + BATCH_SIZE]
        insert_movie_batch(batch)
        inserted += len(batch)

        print(
            f"[build_graph] Inserted {inserted}/{len(movies)} movies...",
            flush=True,
        )

    print(f"[build_graph] Inserted graph data for {inserted} movies.", flush=True)

    node_count = run_cypher("MATCH (n) RETURN count(n) AS count")
    rel_count = run_cypher("MATCH ()-[r]->() RETURN count(r) AS count")

    print(f"[build_graph] Neo4j node count: {node_count}", flush=True)
    print(f"[build_graph] Neo4j relationship count: {rel_count}", flush=True)


def ingest_chroma(data_dir: str):
    print("[build_graph] Ingesting data into ChromaDB...", flush=True)

    try:
        collection = get_collection()
        print(
            f"[build_graph] Chroma collection currently has {collection.count()} items.",
            flush=True,
        )
    except Exception as e:
        print(
            f"[build_graph] Could not inspect Chroma collection before indexing: {e}",
            flush=True,
        )

    index_folder(folder=data_dir)

    try:
        collection = get_collection()
        print(
            f"[build_graph] Chroma collection now has {collection.count()} items.",
            flush=True,
        )
    except Exception as e:
        print(
            f"[build_graph] Could not inspect Chroma collection after indexing: {e}",
            flush=True,
        )


def main():
    load_dotenv()

    try:
        print("[build_graph] Starting ingestion pipeline...", flush=True)
        print(f"[build_graph] TMDB_DATA_DIR = {settings.TMDB_DATA_DIR}", flush=True)
        print(f"[build_graph] TMDB_PAGES = {settings.TMDB_PAGES}", flush=True)

        print("[build_graph] Fetching TMDB data...", flush=True)
        fetch_tmdb_data(pages=settings.TMDB_PAGES)

        setup_neo4j_schema()

        build_and_insert_graph(settings.TMDB_DATA_DIR)

        ingest_chroma(settings.TMDB_DATA_DIR)

        print("[build_graph] Ingestion pipeline complete.", flush=True)

    finally:
        close_driver()




if __name__ == "__main__":
    main()
