import os

# ─ Data source
DATA_FOLDER   = "tmdb_raw_data"
OUT_DIR       = DATA_FOLDER
TMDB_DATA_DIR = DATA_FOLDER

# ─ Neo4j
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "passpass")

# ─ Ollama
MODEL_URL = os.getenv("MODEL_URL", "http://localhost:11434")
MODEL_ID  = os.getenv("MODEL_ID",  "qwen2.5:7b")

# ─ ChromaDB
CHROMA_PATH       = os.getenv("CHROMA_PATH",       "chroma_db")
CHROMA_HOST       = os.getenv("CHROMA_HOST",       None)
CHROMA_PORT       = int(os.getenv("CHROMA_PORT",   "8000"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "movies")
EMBEDDING_MODEL   = os.getenv("EMBEDDING_MODEL",   "all-MiniLM-L6-v2")
CHUNK_SIZE        = int(os.getenv("CHUNK_SIZE",    "3000"))

# ─ TMDB
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_PAGES    = int(os.getenv("TMDB_PAGES", "3"))
# ─ Neo4j schema 
NEO4J_SCHEMA = """
- (Person)-[:DIRECTED]->(Movie)
- (Person)-[:ACTED_IN]->(Movie)
- (Movie)-[:HAS_GENRE]->(Genre)
- (Movie)-[:HAS_KEYWORD]->(Keyword)
- All names are case-sensitive and title-cased e.g. 'Action' not 'action'
"""

# Allowed relationship types when inserting free-text edges.
ALLOWED_REL_TYPES = {"DIRECTED", "ACTED_IN", "HAS_GENRE", "HAS_KEYWORD"}

# ─ Prompts ─
INTENT_PROMPT = """\
Given this question about movies, extract:
1. The intent (e.g. find movies, find directors, count, recommend)
2. Any specific names mentioned (movies, people, genres, keywords)

Reply in this exact format:
INTENT: <intent>
ENTITIES: <comma separated names or NONE>

Question: {question}"""

CYPHER_PROMPT = """\
You are a Neo4j expert. Write a Cypher query for this movie question.

SCHEMA:
{schema}

CRITICAL CYPHER RULES:
- Return ONLY a valid Cypher query.
- Use ONLY these labels: Person, Movie, Genre, Keyword.
- Use ONLY these relationships: DIRECTED, ACTED_IN, HAS_GENRE, HAS_KEYWORD.
- Use ONLY the property `name`.
- Movie titles are stored as m.name.
- Person names are stored as p.name.
- Genre names are stored as g.name.
- Keyword names are stored as k.name.
- Do NOT invent labels, properties, or relationships.
- Do NOT use Movie.title.
- Do NOT use m.title.
- Do NOT use relationships like FOLLOWS, SEQUEL_TO, PART_OF, BELONGS_TO_COLLECTION, RELEASED_IN, PRODUCED_BY.
- Cypher does NOT have GROUP BY or HAVING. Use WITH for aggregation filtering.
- If the question asks for title patterns, use m.name and string functions.
- For case-insensitive matching, use toLower().
- For exact matching, use n.name = 'Name Here'.

VALID EXAMPLES:

Q: Which directors directed more than one movie?
A: MATCH (p:Person)-[:DIRECTED]->(m:Movie) WITH p, count(m) AS c WHERE c > 1 RETURN p.name, c ORDER BY c DESC LIMIT 10

Q: Which movie has the most keywords?
A: MATCH (m:Movie)-[:HAS_KEYWORD]->(k:Keyword) WITH m, count(k) AS c RETURN m.name, c ORDER BY c DESC LIMIT 10

Q: What genres does Sam Raimi work in?
A: MATCH (p:Person {{name: 'Sam Raimi'}})-[:DIRECTED]->(m:Movie)-[:HAS_GENRE]->(g:Genre) RETURN DISTINCT g.name LIMIT 10

Q: Which actors acted in Mortal Kombat?
A: MATCH (p:Person)-[:ACTED_IN]->(m:Movie) WHERE toLower(m.name) = toLower('Mortal Kombat') RETURN p.name LIMIT 20

Q: Which movies have the genre Action?
A: MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre) WHERE g.name = 'Action' RETURN m.name LIMIT 20

Q: Which movies contain the number 2 in the title?
A: MATCH (m:Movie) WHERE m.name CONTAINS '2' RETURN m.name LIMIT 50

Q: Which movies contain Avatar in the title?
A: MATCH (m:Movie) WHERE toLower(m.name) CONTAINS toLower('Avatar') RETURN m.name LIMIT 20

Q: Which movies have both Action and Science Fiction genres?
A: MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre) WHERE g.name IN ['Action', 'Science Fiction'] WITH m, collect(DISTINCT g.name) AS genres WHERE all(x IN ['Action', 'Science Fiction'] WHERE x IN genres) RETURN m.name LIMIT 20

INTENT ANALYSIS:
{intent}

QUESTION: {question}

Return ONLY the Cypher query, no markdown, no backticks, no explanation.
Cypher:"""


CYPHER_FIX_PROMPT = """\
This Cypher failed: {cypher}
Error: {error}

REMEMBER: Cypher has no GROUP BY or HAVING. Use WITH to filter aggregations:
MATCH (p:Person)-[:DIRECTED]->(m:Movie) WITH p, count(m) AS c WHERE c > 1 RETURN p.name, c

Return ONLY the fixed Cypher."""

NEO4J_ANSWER_PROMPT = """\
You are a movie expert. Answer this question using the graph database results below.

QUESTION: {question}

GRAPH RESULTS:
{records}

Give a clear, direct answer based only on these results. \
If empty, say the information was not found in the graph."""

SEARCH_QUERY_PROMPT = """\
You are a search query optimizer for a movie vector database.
Given the intent and question, generate the best possible search query to retrieve relevant movies.
- Be specific and include genre, themes, character types, mood, or keywords
- Do NOT include filler words
- Return ONLY the search query string, nothing else

INTENT ANALYSIS:
{intent}

QUESTION: {question}

Search query:"""

CHROMA_ANSWER_PROMPT = """\
You are a movie expert. Based on the following movies retrieved from a database, \
answer the user's question.

MOVIES:
{context}

QUESTION: {question}

Give a clear, direct answer based only on the movies provided. \
If the information is not found, say so."""
