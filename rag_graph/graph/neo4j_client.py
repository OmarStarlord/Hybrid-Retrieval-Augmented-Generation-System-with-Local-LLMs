from neo4j import GraphDatabase
from config import settings


# ── connection ────────────────────────────────────────────────────────────────

_driver = None


def get_driver(uri=None, user=None, password=None):
    """
    Return a reusable Neo4j driver.

    If custom uri/user/password are supplied, create a temporary separate driver.
    Otherwise reuse the global application driver.
    """
    global _driver

    if uri or user or password:
        return GraphDatabase.driver(
            uri or settings.NEO4J_URI,
            auth=(
                user or settings.NEO4J_USER,
                password or settings.NEO4J_PASSWORD,
            ),
        )

    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )

    return _driver


def close_driver():
    """Close the global Neo4j driver."""
    global _driver

    if _driver is not None:
        _driver.close()
        _driver = None


def run_cypher(
    query: str,
    params: dict = None,
    uri=None,
    user=None,
    password=None,
) -> list[dict]:
    """
    Execute a read/write Cypher query and return a list of record dicts.

    Reuses the global Neo4j driver unless custom connection args are passed.
    """
    custom_connection = bool(uri or user or password)
    driver = get_driver(uri, user, password)

    try:
        with driver.session() as session:
            result = session.run(query, parameters=params or {})
            return [record.data() for record in result]
    finally:
        if custom_connection:
            driver.close()


# ── insertion ─────────────────────────────────────────────────────────────────

def _insert_one(tx, movie: str, data: dict, allowed_rel_types: set):
    tx.run("MERGE (m:Movie {name:$m})", m=movie)

    for d in data.get("directors", []):
        tx.run(
            """
            MERGE (p:Person {name:$p})
            SET p:Director
            WITH p
            MATCH (m:Movie {name:$m})
            MERGE (p)-[:DIRECTED]->(m)
            """,
            p=d,
            m=movie,
        )

    for a in data.get("actors", []):
        tx.run(
            """
            MERGE (p:Person {name:$p})
            SET p:Actor
            WITH p
            MATCH (m:Movie {name:$m})
            MERGE (p)-[:ACTED_IN]->(m)
            """,
            p=a,
            m=movie,
        )

    for g in data.get("genres", []):
        tx.run(
            """
            MERGE (g:Genre {name:$g})
            WITH g
            MATCH (m:Movie {name:$m})
            MERGE (m)-[:HAS_GENRE]->(g)
            """,
            g=g,
            m=movie,
        )

    for k in data.get("keywords", []):
        tx.run(
            """
            MERGE (k:Keyword {name:$k})
            WITH k
            MATCH (m:Movie {name:$m})
            MERGE (m)-[:HAS_KEYWORD]->(k)
            """,
            k=k,
            m=movie,
        )

    for frm, to, typ in data.get("edges", []):
        if typ not in allowed_rel_types:
            continue

        tx.run(
            f"""
            MERGE (a:Person {{name:$a}})
            MERGE (b:Movie {{name:$b}})
            MERGE (a)-[:{typ}]->(b)
            """,
            a=frm,
            b=to,
        )


def insert_graph(
    clean_graph: dict,
    allowed_rel_types: set = None,
    uri=None,
    user=None,
    password=None,
) -> None:
    allowed = allowed_rel_types or settings.ALLOWED_REL_TYPES
    custom_connection = bool(uri or user or password)
    driver = get_driver(uri, user, password)

    try:
        with driver.session() as session:
            for movie, data in clean_graph.items():
                session.execute_write(_insert_one, movie, data, allowed)
    finally:
        if custom_connection:
            driver.close()

    print(f"[neo4j_client] Inserted {len(clean_graph)} movies into Neo4j")
