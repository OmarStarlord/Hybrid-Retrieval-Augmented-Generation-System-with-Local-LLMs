import json
import os
import chromadb
from chromadb.utils import embedding_functions
from config import settings


_client = None
_embedding_function = None
_collection = None


def get_client(chroma_path: str = None):
    global _client

    path = chroma_path or settings.CHROMA_PATH

    if _client is None:
        _client = chromadb.PersistentClient(path=path)

    return _client


def get_embedding_function(embedding_model: str = None):
    global _embedding_function

    model = embedding_model or settings.EMBEDDING_MODEL

    if _embedding_function is None:
        _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model
        )

    return _embedding_function


def get_collection(
    chroma_path: str = None,
    collection_name: str = None,
    embedding_model: str = None,
):
    path  = chroma_path     or settings.CHROMA_PATH
    name  = collection_name or settings.CHROMA_COLLECTION
    model = embedding_model or settings.EMBEDDING_MODEL

    if settings.CHROMA_HOST:
        client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
    else:
        client = chromadb.PersistentClient(path=path)

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
    return client.get_or_create_collection(name=name, embedding_function=ef)


def chunk_text(text: str, size: int = None) -> list[str]:
    size = size or settings.CHUNK_SIZE
    return [text[i:i + size] for i in range(0, len(text), size)]


def index_folder(
    folder: str = None,
    collection=None,
    chunk_size: int = None,
) -> int:
    folder = folder or settings.TMDB_DATA_DIR
    collection = collection or get_collection()

    files = [
        f for f in os.listdir(folder)
        if f.endswith(".json") and f != "all.json"
    ]

    total = 0

    for fname in files:
        fpath = os.path.join(folder, fname)

        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[chroma_index] Skipping {fname}: {e}")
                continue

        text = json.dumps(data, ensure_ascii=False)

        chunks = chunk_text(text, chunk_size)
        movie_key = fname.replace(".json", "")

        if not chunks:
            continue

        collection.upsert(
            ids=[f"{movie_key}_{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[
                {
                    "movie": movie_key,
                    "chunk": i,
                    "source_file": fname,
                }
                for i in range(len(chunks))
            ],
        )

        total += len(chunks)
        print(f"[chroma_index] {fname} → {len(chunks)} chunks")

    print(f"[chroma_index] Done — {total} chunks from {len(files)} files")
    return total


def query_collection(
    query: str,
    n_results: int = 5,
    collection=None,
) -> tuple[list[str], list[str]]:
    collection = collection or get_collection()

    res = collection.query(
        query_texts=[query.strip()],
        n_results=n_results,
    )

    documents = res["documents"][0]
    metadatas = res["metadatas"][0]

    titles = [
        m.get("movie", m.get("title", "unknown"))
        for m in metadatas
    ]

    return titles, documents
