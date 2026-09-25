# ChromaDB RAG vs Neo4j RAG Benchmark Report

Generated: 2026-06-01T14:57:36

## Summary

- Total questions: **100**
- Chroma wins: **52** (52.0%)
- Neo4j wins: **27** (27.0%)
- Ties: **3** (3.0%)
- Neither/errors: **18**
- Expected winner matched judge: **75.0%**

## Latency

- Chroma avg: **17.771s**, median: **16.524s**
- Neo4j avg: **14.255s**, median: **12.549s**

## Average LLM Judge Scores

- Chroma: **3.11/5**
- Neo4j: **2.35/5**

## Results by Category

| Category | Total | Chroma | Neo4j | Tie | Neither |
|---|---:|---:|---:|---:|---:|
| aggregation | 12 | 0 | 9 | 0 | 3 |
| graph_traversal | 11 | 1 | 8 | 0 | 2 |
| semantic_similarity | 4 | 4 | 0 | 0 | 0 |
| semantic_theme | 19 | 12 | 2 | 1 | 4 |
| semantic_vibe | 37 | 34 | 0 | 0 | 3 |
| structured_actor_lookup | 2 | 0 | 0 | 0 | 2 |
| structured_cast_lookup | 1 | 0 | 0 | 0 | 1 |
| structured_director_lookup | 2 | 0 | 1 | 0 | 1 |
| structured_genre_lookup | 3 | 0 | 2 | 0 | 1 |
| structured_keyword_lookup | 3 | 0 | 1 | 1 | 1 |
| structured_movie_lookup | 3 | 1 | 1 | 1 | 0 |
| structured_multi_filter | 3 | 0 | 3 | 0 | 0 |

## Per-question Results

| ID | Expected | Winner | Chroma Time | Neo4j Time | Question | Reason |
|---:|---|---|---:|---:|---|---|
| 1 | chroma | chroma | 27.636s | 11.657s | Recommend me something feel-good and lighthearted | ChromaDB provided a relevant and specific movie recommendation, while Neo4j returned no results despite having an appropriate query structure. |
| 2 | chroma | chroma | 26.948s | 15.267s | Find me movies with a similar vibe to Malena | System A provided a more detailed and relevant list of movie suggestions with descriptions that align well with the user's request. System B returned no results, making it less use |
| 3 | chroma | chroma | 17.040s | 20.411s | What should I watch if I want something emotional but not too depressing? | ChromaDB provided a relevant and specific movie recommendation that aligns with the user's preferences. Neo4j returned an error message instead of a valid query result. |
| 4 | chroma | chroma | 18.106s | 14.994s | Suggest a movie that feels nostalgic and romantic | System A provided a relevant set of movie IDs and suggested potential alternatives, which is more useful and specific to the user's request. System B returned no results despite us |
| 5 | chroma | chroma | 16.518s | 11.737s | I want a slow, atmospheric movie with beautiful visuals | ChromaDB provided relevant titles and a descriptive answer, whereas Neo4j returned no results despite a proper query. |
| 6 | chroma | chroma | 15.297s | 12.348s | Recommend something tense and psychological | ChromaDB provides a specific recommendation based on the given movies, whereas Neo4j returns no results despite matching the query. |
| 7 | chroma | chroma | 23.351s | 10.986s | Find movies that feel dreamy and poetic | System A provided relevant movie titles and a reasoned analysis, while System B returned no results despite using an appropriate query. |
| 8 | chroma | chroma | 18.481s | 11.351s | What movies are good for a cozy weekend night? | System A provided relevant movie recommendations based on the context and criteria, while System B returned an empty result despite using a relevant query. |
| 9 | chroma | chroma | 19.659s | 11.660s | Recommend something dark, stylish, and suspenseful | ChromaDB vector RAG provided a specific and relevant movie recommendation that aligns with the question, while Neo4j returned no results despite an appropriate query. |
| 10 | chroma | chroma | 17.857s | 12.481s | Find a movie with a bittersweet coming-of-age feeling | ChromaDB provided relevant movie titles despite not finding a perfect match, while Neo4j returned no results and did not identify the correct entities. |
| 11 | chroma | chroma | 17.856s | 12.059s | Suggest films about complicated love and memory | ChromaDB provided relevant movie recommendations and a clear explanation, while Neo4j returned no results despite a proper query. |
| 12 | chroma | chroma | 18.686s | 11.890s | I want something whimsical but emotionally meaningful | ChromaDB provided a more specific and relevant list of movies, even though it had to infer from existing titles. Neo4j's query did not return any results, making the answer less us |
| 13 | chroma | chroma | 17.537s | 14.115s | Find movies that are quiet, intimate, and character-driven | System A provided a more relevant and specific search query that aligned with the question, while System B's Cypher query did not yield any results despite being more precise in it |
| 14 | chroma | chroma | 23.921s | 13.099s | Recommend a movie about loneliness in a big city | System A provided a more relevant and useful set of recommendations, even though none matched the exact criteria. It also offered an explanation for why no suitable movies were fou |
| 15 | chroma | chroma | 17.107s | 13.363s | What should I watch if I liked the emotional tone of Lost in Translation? | System A provided a relevant movie recommendation based on the emotional tone of 'Lost in Translation,' while System B did not return any results, making its response less useful. |
| 16 | chroma | chroma | 18.160s | 30.204s | Suggest something eerie without being a straightforward horror movie | ChromaDB vector RAG provided a relevant and useful answer that matched the question's intent, while Neo4j's response was focused on resolving a query syntax error rather than addre |
| 17 | chroma | neither | 36.854s | 12.819s | Find films with themes of obsession and identity | Both systems returned empty results, indicating no movies were found that match the exact keywords. However, System A provided more detailed reasoning and context, while System B d |
| 18 | chroma | chroma | 17.413s | 11.706s | Recommend movies that feel warm, funny, and human | ChromaDB provided relevant movie recommendations based on the given criteria, although with some limitations in detail. Neo4j returned no results despite a correct query structure. |
| 19 | chroma | chroma | 18.550s | 12.682s | I want a stylish crime movie with a cool atmosphere | ChromaDB provided relevant movie titles and a reasonable explanation, even though it had to infer some aspects. Neo4j returned no results despite the correct query structure. |
| 20 | chroma | chroma | 16.130s | 13.514s | Find something sad, beautiful, and reflective | ChromaDB provided a relevant and specific movie suggestion that aligns with the question, while Neo4j returned no results. |
| 21 | chroma | neither | 18.852s | 11.313s | Recommend a movie that explores grief in a subtle way | Both systems failed to provide a relevant movie recommendation. ChromaDB's answer is partially coherent but does not actually address the question of subtlety in exploring grief. N |
| 22 | chroma | neither | 18.476s | 11.884s | What movies have a magical, fairy-tale-like mood? | Both systems failed to provide relevant, specific titles of movies with a magical or fairy-tale-like mood. However, ChromaDB provided more context and reasoning based on the availa |
| 23 | chroma | chroma | 29.121s | 14.177s | Find films similar in mood to Amelie | ChromaDB vector RAG provided a relevant and specific set of film recommendations that align with 'Amelie's mood, while Neo4j returned no results despite the correct query structure |
| 24 | chroma | chroma | 19.928s | 13.471s | Recommend something philosophical but still entertaining | ChromaDB provided a more relevant and useful response by narrowing down the options and offering an inference, even though it couldn't pinpoint a specific title. Neo4j returned no  |
| 25 | chroma | chroma | 22.393s | 11.848s | I want a movie about second chances and redemption | System A provided relevant and specific movie recommendations, while System B returned no results despite a valid query. |
| 26 | chroma | chroma | 18.932s | 11.034s | Suggest a film with a strong sense of place and atmosphere | System A provided relevant film suggestions that fit the criteria of strong sense of place and atmosphere. While System B's query did not yield results, it still attempted to addre |
| 27 | chroma | chroma | 15.625s | 12.159s | Find movies that are emotionally intense and visually striking | ChromaDB provided relevant movie titles and a specific answer, whereas Neo4j's query did not return any results. |
| 28 | chroma | chroma | 17.082s | 14.648s | Recommend something clever, playful, and unusual | ChromaDB provided a relevant and specific recommendation with detailed reasoning, while Neo4j returned no results. |
| 29 | chroma | chroma | 15.112s | 10.553s | What should I watch if I want a melancholic romance? | System A provided a relevant and specific movie recommendation based on the query, whereas System B returned no results despite using an appropriate Cypher query. |
| 30 | chroma | chroma | 22.147s | 11.748s | Find movies about friendship that are not cheesy | System A provided a more detailed and relevant search, while System B returned no results despite matching criteria. |
| 31 | chroma | chroma | 15.064s | 12.926s | Suggest a movie with an unsettling small-town atmosphere | ChromaDB provided relevant movie suggestions based on the query, whereas Neo4j's search returned no results. |
| 32 | chroma | chroma | 23.601s | 10.756s | Recommend a film that feels like a memory or dream | ChromaDB provides more relevant and specific recommendations based on the query, while Neo4j fails to find any matches despite a similar approach. |
| 33 | chroma | chroma | 16.198s | 13.443s | Find something adventurous but emotionally grounded | ChromaDB provides a more relevant and specific answer, matching the exact criteria of 'adventurous but emotionally grounded'. Neo4j's query is correct but returns less relevant res |
| 34 | chroma | tie | 15.800s | 12.155s | What movies have a haunting and tragic love story? | Both systems correctly identified the key entities (haunting, tragic love story) and performed relevant searches. However, both returned empty results based on their respective dat |
| 35 | chroma | chroma | 23.724s | 13.158s | Suggest a movie with quiet humor and gentle drama | ChromaDB vector RAG provided a relevant and contextually appropriate suggestion, despite not having an exact match in its database. It also offered reasoning for why the suggested  |
| 36 | chroma | chroma | 17.588s | 13.474s | Find a movie that captures youthful confusion and longing | ChromaDB's response was more relevant and specific to the question, providing a clear explanation for why none of the movies matched the criteria. Neo4j returned an empty result bu |
| 37 | chroma | chroma | 24.838s | 25.916s | Recommend something with moral ambiguity and complex characters | System A provides a relevant movie recommendation that aligns with the criteria of moral ambiguity and complex characters. The answer is detailed and offers context about the film, |
| 38 | chroma | chroma | 20.368s | 12.676s | I want a movie that feels elegant, romantic, and tragic | ChromaDB vector RAG provided more relevant and specific movie titles, even though they may not fully match the requested criteria. Neo4j returned no results despite a well-formed q |
| 39 | chroma | chroma | 25.162s | 13.515s | Find films with a surreal and mysterious atmosphere | ChromaDB provided relevant and specific recommendations based on the given criteria, while Neo4j returned no results despite a properly constructed query. |
| 40 | chroma | neither | 15.107s | 15.616s | Recommend something uplifting without being silly | Both systems failed to directly provide a specific movie recommendation. However, Neo4j's response was more relevant and useful as it provided titles that fit the criteria of being |
| 41 | chroma | neo4j | 16.296s | 15.514s | Suggest a movie about family secrets and emotional tension | System B's query returned more relevant results and suggested a well-known movie that fits the criteria, while System A incorrectly matched a movie about mummies to family secrets  |
| 42 | chroma | chroma | 15.147s | 13.230s | Find a film that feels raw, realistic, and human | ChromaDB vector RAG provided a specific film suggestion with relevant details, while Neo4j returned no results despite the query's relevance. |
| 43 | chroma | neither | 15.913s | 13.481s | What should I watch if I like tragic historical romances? | Both systems failed to provide relevant and specific movie recommendations. ChromaDB returned a list of movies without any clear relevance, while Neo4j's query did not return any r |
| 44 | chroma | chroma | 18.653s | 14.614s | Recommend something fast-paced and fun but not dumb | ChromaDB provided a relevant and specific recommendation that aligns with the user's criteria, while Neo4j returned no results despite a correct query structure. |
| 45 | chroma | chroma | 14.293s | 11.719s | Find movies with a lonely outsider protagonist | ChromaDB provided relevant search terms and returned titles that, while not explicitly matching the description, are more useful for further investigation. Neo4j did not find any m |
| 46 | chroma | chroma | 22.487s | 12.568s | Suggest something that mixes humor with sadness | ChromaDB provided a relevant and specific recommendation that aligns with the question, whereas Neo4j did not find any matches in its database. |
| 47 | chroma | chroma | 17.406s | 11.756s | Recommend a movie with a moody noir feeling | ChromaDB provides a more relevant and specific answer, suggesting 'The Long Goodbye' which matches the mood. Neo4j's query returns no results despite there being movies with those  |
| 48 | chroma | chroma | 16.576s | 12.440s | Find movies that are romantic but unconventional | System A provided relevant titles that, although not perfectly matching 'unconventional', offered a reasonable interpretation. System B's query did not yield results and the answer |
| 49 | chroma | neo4j | 14.237s | 13.676s | I want a reflective film about aging and regret | Neo4j provided a more specific and relevant answer by querying the graph database directly, while ChromaDB returned a list of movie IDs without clear relevance to the question. |
| 50 | chroma | chroma | 23.942s | 11.135s | Suggest films that feel emotionally honest | System A provided specific film recommendations based on the query, while System B did not find any matches despite using a relevant query. While System A's answer contains some fa |
| 51 | chroma | chroma | 19.351s | 12.617s | Recommend something with dark comedy and social satire | ChromaDB provided relevant titles, even though none strictly fit both categories. Neo4j returned an empty result despite a correct query structure. |
| 52 | chroma | chroma | 18.087s | 15.557s | Find movies similar in feeling to Cinema Paradiso | ChromaDB vector RAG provided a more relevant and specific list of movies with similar feelings, even though it couldn't pinpoint exact matches. Neo4j's approach was less effective  |
| 53 | chroma | chroma | 18.944s | 12.529s | What should I watch for a romantic European art-house mood? | Answer A provided specific movie recommendations based on the given data, even though it had to infer some qualities. Answer B did not find any matching records in its query. |
| 54 | chroma | chroma | 23.068s | 17.146s | Suggest a film that is mysterious, emotional, and slow-burning | ChromaDB provides a relevant suggestion despite limitations, while Neo4j fails to return any results. |
| 55 | chroma | chroma | 16.374s | 10.681s | Find movies about forbidden love | System A provided a more specific and relevant search query that yielded some results, even if they did not fully match the intent. System B's query did not return any records, mak |
| 56 | chroma | chroma | 15.962s | 14.902s | Recommend something that feels grand, epic, and emotional | ChromaDB's answer is more specific and directly addresses the emotional and epic nature of the recommendation, while Neo4j provides a broader list without strong justification. |
| 57 | chroma | neither | 15.726s | 13.004s | I want a movie with a charming but flawed main character | Both systems failed to provide relevant movie recommendations based on the given criteria. ChromaDB returned a generic response without any specific titles, while Neo4j's query did |
| 58 | chroma | chroma | 13.909s | 11.643s | Find movies with a hopeful ending after hardship | ChromaDB provided a more relevant and useful answer by identifying movies that fit the criteria of a hopeful ending after hardship, even though it could not find explicit informati |
| 59 | chroma | chroma | 16.405s | 30.091s | Suggest a film that explores jealousy and desire | ChromaDB's response provides a specific movie title and relevant plot details, making it more useful and directly answering the question. Neo4j's answer focuses on correcting a Cyp |
| 60 | chroma | neither | 16.461s | 12.316s | Recommend a movie that feels tender and sad | Both systems failed to provide a specific movie recommendation. However, System B attempted to query the graph with a relevant Cypher query but returned no results, while System A  |
| 61 | neo4j | neo4j | 13.605s | 15.969s | Which movies have Action as a genre? | Neo4j's answer is more accurate, relevant, and specific to the question. It provides a detailed list of movies with Action as a genre based on its graph database query, while Chrom |
| 62 | neo4j | neo4j | 15.717s | 12.212s | What genres does Sam Raimi work in? | System B (Neo4j) provides a more specific and direct answer by querying the graph database with Cypher, which aligns well with the question. The answer includes genres from the que |
| 63 | neo4j | neo4j | 13.922s | 11.527s | Which movie has the most keywords tagged to it? | Neo4j provided a more detailed and specific answer with the exact movie name, number of keywords, and even returned multiple movies for context. ChromaDB's response was less accura |
| 64 | neo4j | neo4j | 14.279s | 12.125s | List movies in the Comedy genre | System B provided a specific and relevant Cypher query, fetched actual movie titles from the graph database, and accurately reported the results. System A's answer was not accurate |
| 65 | neo4j | neo4j | 17.668s | 16.651s | Which people directed movies in the Horror genre? | Neo4j provided a relevant and specific answer using a Cypher query, whereas ChromaDB's response was incomplete and less accurate. |
| 66 | neo4j | tie | 12.145s | 11.010s | Which movies are connected to the keyword romance? | Both systems returned no results for the query, indicating they did not find any movies connected to the keyword romance in their respective databases. Neither system provided a re |
| 67 | neo4j | neither | 13.328s | 11.190s | What actors appeared in Spider-Man? | Both systems failed to provide a relevant list of actors. However, Neo4j provided a more specific query that could potentially yield results if the graph contained such data, where |
| 68 | neo4j | neo4j | 13.742s | 10.993s | Who directed Spider-Man? | Neo4j provided a more specific and relevant approach using Cypher queries, while ChromaDB returned a generic answer without leveraging the structured data. Neo4j's query directly s |
| 69 | neo4j | neither | 15.584s | 11.146s | Which movies did Kirsten Dunst act in? | Both systems failed to provide useful, relevant, and specific information. However, Neo4j attempted to use a more structured approach with a Cypher query, which is closer to the ex |
| 70 | neo4j | chroma | 12.282s | 10.852s | Which genres are attached to Malena? | ChromaDB returned a relevant and specific answer, correctly identifying the genre as Drama. Neo4j's query did not return any results, indicating that either the data was missing or |
| 71 | neo4j | neither | 16.879s | 11.874s | Which movies share a genre with Malena? | ChromaDB returned a search query and relevant movie genres, while Neo4j attempted to find movies sharing the same genre but did not match any. Neither provided directly comparable  |
| 72 | neo4j | chroma | 21.466s | 42.833s | Which movies share keywords with Malena? | ChromaDB vector RAG provided a relevant and useful answer based on the available data, whereas Neo4j's response contained a syntax error in its query. |
| 73 | neo4j | neo4j | 18.609s | 12.151s | Which genre has the most movies? | Neo4j's answer is more specific, relevant, and correct. It provides a direct query result to determine the genre with the most movies, whereas ChromaDB only analyzes a small set of |
| 74 | neo4j | neo4j | 29.060s | 15.971s | Which actor appears in the most movies? | Neo4j provided a relevant and specific query to find the most prolific actor, whereas ChromaDB's answer was based on limited data and did not address the question fully. |
| 75 | neo4j | neo4j | 14.597s | 13.848s | Which director has directed the most movies? | Neo4j provided a specific query and returned relevant results, while ChromaDB did not provide useful information based on the data. |
| 76 | neo4j | neo4j | 14.772s | 15.136s | Show movies that are both Drama and Romance | Neo4j's approach using Cypher queries is more specific and relevant to finding movies that belong to both genres. ChromaDB's response lacks the ability to accurately find such over |
| 77 | neo4j | neo4j | 12.741s | 15.214s | Show movies that are both Action and Adventure | Neo4j's query is more specific and relevant to the question, providing a structured approach to finding movies that are both Action and Adventure. ChromaDB does not match the expec |
| 78 | neo4j | neo4j | 15.963s | 11.808s | Which people worked on movies tagged with friendship? | Neo4j's query is more relevant and specific to the question, leveraging graph relationships effectively. ChromaDB provides a vague answer without addressing the tag 'friendship' or |
| 79 | neo4j | neo4j | 16.151s | 13.411s | Which movies are tagged with both love and jealousy? | Neo4j's query correctly uses graph database principles to find movies associated with both 'love' and 'jealousy', while ChromaDB provides a less precise search that does not yield  |
| 80 | neo4j | tie | 13.905s | 10.849s | What keywords are connected to The Godfather? | Both systems failed to provide relevant keywords for 'The Godfather' and returned generic messages indicating that no information was found. Neither system demonstrated a clear und |
| 81 | neo4j | neo4j | 16.329s | 10.973s | What genres are connected to The Godfather? | System B correctly used a graph query to find the genres of 'The Godfather', whereas System A provided irrelevant movie IDs and could not answer the question. Neo4j's approach is m |
| 82 | neo4j | neither | 13.814s | 11.038s | Which movies did Francis Ford Coppola direct? | Both systems failed to provide relevant movie titles directed by Francis Ford Coppola. However, Neo4j's approach using a graph query is more aligned with the question type and coul |
| 83 | neo4j | neither | 21.634s | 13.512s | Which actors worked with Francis Ford Coppola? | ChromaDB vector RAG provided an answer based on available data, even though it did not find direct evidence of actors working with Francis Ford Coppola. However, the Neo4j graph RA |
| 84 | neo4j | neo4j | 14.089s | 11.779s | Which directors have worked with Al Pacino? | Neo4j provides a specific query that aligns with the question and returns relevant information, even if no results are found. ChromaDB does not provide an answer based on the given |
| 85 | neo4j | neither | 12.177s | 11.050s | Which movies include Al Pacino? | Both systems failed to provide relevant and specific answers. ChromaDB returned a misleading statement that none of the movies include Al Pacino, while Neo4j correctly formulated a |
| 86 | neo4j | neither | 15.268s | 17.424s | Count how many movies are in each genre | System A provides a relevant count of movies in each genre based on the provided titles, but it does not fully address the question as it only counts for the given titles. System B |
| 87 | neo4j | neo4j | 14.688s | 27.482s | Count how many keywords each movie has | Neo4j provided a detailed and specific answer with exact keyword counts for multiple movies, whereas ChromaDB only provided counts for a few movies without context or relevance. |
| 88 | neo4j | neo4j | 13.737s | 12.291s | Which keyword is used by the most movies? | Neo4j provided a relevant, specific answer using graph database querying to find the most frequently used keyword. ChromaDB did not provide useful information about the movies or t |
| 89 | neo4j | neo4j | 13.541s | 20.533s | Find actors who appeared in more than one movie | Neo4j provided a correct and specific answer using Cypher queries, while ChromaDB failed to provide relevant information. |
| 90 | neo4j | neo4j | 25.184s | 38.058s | Find directors who directed movies in more than one genre | System B correctly provides a Cypher query that, with proper adjustments, would solve the problem. System A's answer is more relevant and useful but lacks the correct implementatio |
| 91 | neo4j | neo4j | 17.086s | 10.642s | Which movies are connected to the keyword mafia? | Neo4j's answer is more relevant and specific as it uses a graph query to find movies connected to the keyword 'mafia'. ChromaDB, while attempting to provide related titles, does no |
| 92 | neo4j | neo4j | 14.492s | 13.709s | Which genres does Al Pacino appear in? | Neo4j's approach using Cypher queries is more specific and relevant to finding Al Pacino's genres, even though it did not find any records. ChromaDB provided a vague response that  |
| 93 | neo4j | neo4j | 18.114s | 15.361s | Which people are connected to both Crime and Drama movies? | Neo4j's answer is more specific, relevant, and directly addresses the question by using a graph query to find people connected to both Crime and Drama movies. ChromaDB's response i |
| 94 | neo4j | neither | 14.205s | 11.827s | Which movies have exactly the genre Drama? | Both systems failed to directly address the exact genre requirement. ChromaDB returned irrelevant titles, while Neo4j provided a mix of titles without explicitly stating that no mo |
| 95 | neo4j | neo4j | 12.855s | 12.002s | Which movies have the fewest keywords? | Neo4j provided a detailed and specific answer with exact movie titles and keyword counts, while ChromaDB failed to provide any useful information. |
| 96 | neo4j | neo4j | 15.542s | 12.146s | Which actors co-starred with Tobey Maguire? | Neo4j provides a Cypher query that is relevant and specific to the question, whereas ChromaDB returns irrelevant information. Neo4j's answer indicates it attempted to find co-stars |
| 97 | neo4j | neo4j | 16.531s | 11.260s | Which directors made movies tagged with superhero? | Neo4j's query is more specific and structured, leading to a clearer understanding of how the search was conducted. While ChromaDB provided a list of movie titles without clear rele |
| 98 | neo4j | neither | 15.721s | 10.265s | Which movies are tagged with superhero? | ChromaDB provided a relevant answer despite it not being explicitly marked as a superhero movie, while Neo4j failed to find any matches in the graph. |
| 99 | neo4j | neither | 13.596s | 12.693s | Which genres are most common among movies starring Tobey Maguire? | Both systems failed to provide a useful answer, but Neo4j's attempt was more relevant and specific using a graph query. However, since neither system returned the expected results  |
| 100 | neo4j | neither | 14.627s | 29.201s | Which movie has the largest number of connected people? | ChromaDB did not provide a relevant answer to the question, while Neo4j provided an explanation of how to write a correct Cypher query but encountered syntax issues. Neither system |

## Notes

- Semantic/vibe/theme questions are expected to favor ChromaDB vector retrieval.
- Exact relationship, filtering, traversal, and aggregation questions are expected to favor Neo4j graph retrieval.
- The judge is LLM-based, so treat results as directional, not absolute ground truth.
- Inspect the CSV/JSONL files for full raw answers and errors.