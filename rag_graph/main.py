import csv
import json
import statistics
import time
from datetime import datetime
from pathlib import Path

from rag.chroma_rag import chroma_rag
from rag.neo4j_rag import neo4j_rag
from graph.neo4j_client import run_cypher
from utils.llm import llm


QUESTIONS = [
    
    {"id": 1, "question": "Recommend me something feel-good and lighthearted", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 2, "question": "Find me movies with a similar vibe to Malena", "category": "semantic_similarity", "expected_winner": "chroma"},
    {"id": 3, "question": "What should I watch if I want something emotional but not too depressing?", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 4, "question": "Suggest a movie that feels nostalgic and romantic", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 5, "question": "I want a slow, atmospheric movie with beautiful visuals", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 6, "question": "Recommend something tense and psychological", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 7, "question": "Find movies that feel dreamy and poetic", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 8, "question": "What movies are good for a cozy weekend night?", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 9, "question": "Recommend something dark, stylish, and suspenseful", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 10, "question": "Find a movie with a bittersweet coming-of-age feeling", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 11, "question": "Suggest films about complicated love and memory", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 12, "question": "I want something whimsical but emotionally meaningful", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 13, "question": "Find movies that are quiet, intimate, and character-driven", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 14, "question": "Recommend a movie about loneliness in a big city", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 15, "question": "What should I watch if I liked the emotional tone of Lost in Translation?", "category": "semantic_similarity", "expected_winner": "chroma"},
    {"id": 16, "question": "Suggest something eerie without being a straightforward horror movie", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 17, "question": "Find films with themes of obsession and identity", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 18, "question": "Recommend movies that feel warm, funny, and human", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 19, "question": "I want a stylish crime movie with a cool atmosphere", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 20, "question": "Find something sad, beautiful, and reflective", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 21, "question": "Recommend a movie that explores grief in a subtle way", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 22, "question": "What movies have a magical, fairy-tale-like mood?", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 23, "question": "Find films similar in mood to Amelie", "category": "semantic_similarity", "expected_winner": "chroma"},
    {"id": 24, "question": "Recommend something philosophical but still entertaining", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 25, "question": "I want a movie about second chances and redemption", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 26, "question": "Suggest a film with a strong sense of place and atmosphere", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 27, "question": "Find movies that are emotionally intense and visually striking", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 28, "question": "Recommend something clever, playful, and unusual", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 29, "question": "What should I watch if I want a melancholic romance?", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 30, "question": "Find movies about friendship that are not cheesy", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 31, "question": "Suggest a movie with an unsettling small-town atmosphere", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 32, "question": "Recommend a film that feels like a memory or dream", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 33, "question": "Find something adventurous but emotionally grounded", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 34, "question": "What movies have a haunting and tragic love story?", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 35, "question": "Suggest a movie with quiet humor and gentle drama", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 36, "question": "Find a movie that captures youthful confusion and longing", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 37, "question": "Recommend something with moral ambiguity and complex characters", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 38, "question": "I want a movie that feels elegant, romantic, and tragic", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 39, "question": "Find films with a surreal and mysterious atmosphere", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 40, "question": "Recommend something uplifting without being silly", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 41, "question": "Suggest a movie about family secrets and emotional tension", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 42, "question": "Find a film that feels raw, realistic, and human", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 43, "question": "What should I watch if I like tragic historical romances?", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 44, "question": "Recommend something fast-paced and fun but not dumb", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 45, "question": "Find movies with a lonely outsider protagonist", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 46, "question": "Suggest something that mixes humor with sadness", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 47, "question": "Recommend a movie with a moody noir feeling", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 48, "question": "Find movies that are romantic but unconventional", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 49, "question": "I want a reflective film about aging and regret", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 50, "question": "Suggest films that feel emotionally honest", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 51, "question": "Recommend something with dark comedy and social satire", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 52, "question": "Find movies similar in feeling to Cinema Paradiso", "category": "semantic_similarity", "expected_winner": "chroma"},
    {"id": 53, "question": "What should I watch for a romantic European art-house mood?", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 54, "question": "Suggest a film that is mysterious, emotional, and slow-burning", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 55, "question": "Find movies about forbidden love", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 56, "question": "Recommend something that feels grand, epic, and emotional", "category": "semantic_vibe", "expected_winner": "chroma"},
    {"id": 57, "question": "I want a movie with a charming but flawed main character", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 58, "question": "Find movies with a hopeful ending after hardship", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 59, "question": "Suggest a film that explores jealousy and desire", "category": "semantic_theme", "expected_winner": "chroma"},
    {"id": 60, "question": "Recommend a movie that feels tender and sad", "category": "semantic_vibe", "expected_winner": "chroma"},

    # Expected Neo4j wins: structured graph lookup / traversal / aggregation
    {"id": 61, "question": "Which movies have Action as a genre?", "category": "structured_genre_lookup", "expected_winner": "neo4j"},
    {"id": 62, "question": "What genres does Sam Raimi work in?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 63, "question": "Which movie has the most keywords tagged to it?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 64, "question": "List movies in the Comedy genre", "category": "structured_genre_lookup", "expected_winner": "neo4j"},
    {"id": 65, "question": "Which people directed movies in the Horror genre?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 66, "question": "Which movies are connected to the keyword romance?", "category": "structured_keyword_lookup", "expected_winner": "neo4j"},
    {"id": 67, "question": "What actors appeared in Spider-Man?", "category": "structured_cast_lookup", "expected_winner": "neo4j"},
    {"id": 68, "question": "Who directed Spider-Man?", "category": "structured_director_lookup", "expected_winner": "neo4j"},
    {"id": 69, "question": "Which movies did Kirsten Dunst act in?", "category": "structured_actor_lookup", "expected_winner": "neo4j"},
    {"id": 70, "question": "Which genres are attached to Malena?", "category": "structured_movie_lookup", "expected_winner": "neo4j"},
    {"id": 71, "question": "Which movies share a genre with Malena?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 72, "question": "Which movies share keywords with Malena?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 73, "question": "Which genre has the most movies?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 74, "question": "Which actor appears in the most movies?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 75, "question": "Which director has directed the most movies?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 76, "question": "Show movies that are both Drama and Romance", "category": "structured_multi_filter", "expected_winner": "neo4j"},
    {"id": 77, "question": "Show movies that are both Action and Adventure", "category": "structured_multi_filter", "expected_winner": "neo4j"},
    {"id": 78, "question": "Which people worked on movies tagged with friendship?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 79, "question": "Which movies are tagged with both love and jealousy?", "category": "structured_multi_filter", "expected_winner": "neo4j"},
    {"id": 80, "question": "What keywords are connected to The Godfather?", "category": "structured_movie_lookup", "expected_winner": "neo4j"},
    {"id": 81, "question": "What genres are connected to The Godfather?", "category": "structured_movie_lookup", "expected_winner": "neo4j"},
    {"id": 82, "question": "Which movies did Francis Ford Coppola direct?", "category": "structured_director_lookup", "expected_winner": "neo4j"},
    {"id": 83, "question": "Which actors worked with Francis Ford Coppola?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 84, "question": "Which directors have worked with Al Pacino?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 85, "question": "Which movies include Al Pacino?", "category": "structured_actor_lookup", "expected_winner": "neo4j"},
    {"id": 86, "question": "Count how many movies are in each genre", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 87, "question": "Count how many keywords each movie has", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 88, "question": "Which keyword is used by the most movies?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 89, "question": "Find actors who appeared in more than one movie", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 90, "question": "Find directors who directed movies in more than one genre", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 91, "question": "Which movies are connected to the keyword mafia?", "category": "structured_keyword_lookup", "expected_winner": "neo4j"},
    {"id": 92, "question": "Which genres does Al Pacino appear in?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 93, "question": "Which people are connected to both Crime and Drama movies?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 94, "question": "Which movies have exactly the genre Drama?", "category": "structured_genre_lookup", "expected_winner": "neo4j"},
    {"id": 95, "question": "Which movies have the fewest keywords?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 96, "question": "Which actors co-starred with Tobey Maguire?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 97, "question": "Which directors made movies tagged with superhero?", "category": "graph_traversal", "expected_winner": "neo4j"},
    {"id": 98, "question": "Which movies are tagged with superhero?", "category": "structured_keyword_lookup", "expected_winner": "neo4j"},
    {"id": 99, "question": "Which genres are most common among movies starring Tobey Maguire?", "category": "aggregation", "expected_winner": "neo4j"},
    {"id": 100, "question": "Which movie has the largest number of connected people?", "category": "aggregation", "expected_winner": "neo4j"},
]


def now_stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def safe_call(fn, question):
    start = time.perf_counter()
    try:
        answer = fn(question)
        elapsed = time.perf_counter() - start
        return {
            "ok": True,
            "answer": str(answer),
            "error": "",
            "time_sec": elapsed,
            "answer_chars": len(str(answer)),
        }
    except Exception as e:
        elapsed = time.perf_counter() - start
        return {
            "ok": False,
            "answer": "",
            "error": repr(e),
            "time_sec": elapsed,
            "answer_chars": 0,
        }


def judge_answer(question, expected_winner, chroma_answer, neo4j_answer):
    prompt = f"""
You are judging two RAG systems for a movie QA/recommendation benchmark.

Question: {question}
Expected stronger system by question type: {expected_winner}

System A: ChromaDB vector RAG
Answer A:
{chroma_answer}

System B: Neo4j graph RAG
Answer B:
{neo4j_answer}

Return STRICT JSON only with this schema:
{{
  "winner": "chroma" | "neo4j" | "tie" | "neither",
  "chroma_score": integer 0-5,
  "neo4j_score": integer 0-5,
  "reason": "short reason"
}}

Judge by correctness, usefulness, relevance, specificity, and whether the answer fits the question.
Do not automatically pick the expected system; use the actual answers.
"""
    try:
        raw = llm(prompt)
        text = str(raw).strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()
        data = json.loads(text)
        return {
            "winner": data.get("winner", "neither"),
            "chroma_score": int(data.get("chroma_score", 0)),
            "neo4j_score": int(data.get("neo4j_score", 0)),
            "judge_reason": data.get("reason", ""),
            "judge_raw": text,
        }
    except Exception as e:
        return {
            "winner": "judge_error",
            "chroma_score": 0,
            "neo4j_score": 0,
            "judge_reason": repr(e),
            "judge_raw": "",
        }


def write_csv(path, rows):
    fieldnames = [
        "id", "category", "expected_winner", "question",
        "chroma_ok", "chroma_time_sec", "chroma_answer_chars", "chroma_error", "chroma_answer",
        "neo4j_ok", "neo4j_time_sec", "neo4j_answer_chars", "neo4j_error", "neo4j_answer",
        "faster_system", "time_delta_sec",
        "judge_winner", "expected_matched", "chroma_score", "neo4j_score", "judge_reason",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    total = len(rows)
    chroma_wins = sum(1 for r in rows if r["judge_winner"] == "chroma")
    neo4j_wins = sum(1 for r in rows if r["judge_winner"] == "neo4j")
    ties = sum(1 for r in rows if r["judge_winner"] == "tie")
    neither = sum(1 for r in rows if r["judge_winner"] in ("neither", "judge_error"))
    expected_matches = sum(1 for r in rows if r["expected_matched"])

    chroma_times = [r["chroma_time_sec"] for r in rows if r["chroma_ok"]]
    neo4j_times = [r["neo4j_time_sec"] for r in rows if r["neo4j_ok"]]
    chroma_scores = [r["chroma_score"] for r in rows]
    neo4j_scores = [r["neo4j_score"] for r in rows]

    by_category = {}
    for r in rows:
        c = r["category"]
        by_category.setdefault(c, {"total": 0, "chroma": 0, "neo4j": 0, "tie": 0, "neither": 0})
        by_category[c]["total"] += 1
        if r["judge_winner"] in by_category[c]:
            by_category[c][r["judge_winner"]] += 1
        else:
            by_category[c]["neither"] += 1

    def avg(xs):
        return statistics.mean(xs) if xs else 0

    def med(xs):
        return statistics.median(xs) if xs else 0

    return {
        "total_questions": total,
        "judge_wins": {
            "chroma": chroma_wins,
            "neo4j": neo4j_wins,
            "tie": ties,
            "neither_or_error": neither,
        },
        "win_rates": {
            "chroma": chroma_wins / total if total else 0,
            "neo4j": neo4j_wins / total if total else 0,
            "tie": ties / total if total else 0,
        },
        "expected_match_rate": expected_matches / total if total else 0,
        "latency": {
            "chroma_avg_sec": avg(chroma_times),
            "chroma_median_sec": med(chroma_times),
            "neo4j_avg_sec": avg(neo4j_times),
            "neo4j_median_sec": med(neo4j_times),
        },
        "scores": {
            "chroma_avg_score": avg(chroma_scores),
            "neo4j_avg_score": avg(neo4j_scores),
        },
        "by_category": by_category,
    }


def markdown_report(summary, rows):
    lines = []
    lines.append("# ChromaDB RAG vs Neo4j RAG Benchmark Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total questions: **{summary['total_questions']}**")
    lines.append(f"- Chroma wins: **{summary['judge_wins']['chroma']}** ({summary['win_rates']['chroma']:.1%})")
    lines.append(f"- Neo4j wins: **{summary['judge_wins']['neo4j']}** ({summary['win_rates']['neo4j']:.1%})")
    lines.append(f"- Ties: **{summary['judge_wins']['tie']}** ({summary['win_rates']['tie']:.1%})")
    lines.append(f"- Neither/errors: **{summary['judge_wins']['neither_or_error']}**")
    lines.append(f"- Expected winner matched judge: **{summary['expected_match_rate']:.1%}**")
    lines.append("")
    lines.append("## Latency")
    lines.append("")
    lines.append(f"- Chroma avg: **{summary['latency']['chroma_avg_sec']:.3f}s**, median: **{summary['latency']['chroma_median_sec']:.3f}s**")
    lines.append(f"- Neo4j avg: **{summary['latency']['neo4j_avg_sec']:.3f}s**, median: **{summary['latency']['neo4j_median_sec']:.3f}s**")
    lines.append("")
    lines.append("## Average LLM Judge Scores")
    lines.append("")
    lines.append(f"- Chroma: **{summary['scores']['chroma_avg_score']:.2f}/5**")
    lines.append(f"- Neo4j: **{summary['scores']['neo4j_avg_score']:.2f}/5**")
    lines.append("")
    lines.append("## Results by Category")
    lines.append("")
    lines.append("| Category | Total | Chroma | Neo4j | Tie | Neither |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for cat, vals in sorted(summary["by_category"].items()):
        lines.append(f"| {cat} | {vals['total']} | {vals['chroma']} | {vals['neo4j']} | {vals['tie']} | {vals['neither']} |")
    lines.append("")
    lines.append("## Per-question Results")
    lines.append("")
    lines.append("| ID | Expected | Winner | Chroma Time | Neo4j Time | Question | Reason |")
    lines.append("|---:|---|---|---:|---:|---|---|")
    for r in rows:
        q = str(r["question"]).replace("|", "\\|")
        reason = str(r["judge_reason"]).replace("|", "\\|")[:180]
        lines.append(f"| {r['id']} | {r['expected_winner']} | {r['judge_winner']} | {r['chroma_time_sec']:.3f}s | {r['neo4j_time_sec']:.3f}s | {q} | {reason} |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Semantic/vibe/theme questions are expected to favor ChromaDB vector retrieval.")
    lines.append("- Exact relationship, filtering, traversal, and aggregation questions are expected to favor Neo4j graph retrieval.")
    lines.append("- The judge is LLM-based, so treat results as directional, not absolute ground truth.")
    lines.append("- Inspect the CSV/JSONL files for full raw answers and errors.")
    return "\n".join(lines)


def main():
    out_dir = Path("benchmark_results") / now_stamp()
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Health checks")
    print("Neo4j:", run_cypher("RETURN 1 AS test"))
    print("LLM:  ", llm("Say hello in one word."))
    print("=" * 80)
    print("CHROMA RAG vs NEO4J RAG BENCHMARK")
    print(f"Questions: {len(QUESTIONS)}")
    print(f"Output dir: {out_dir}")
    print("=" * 80)

    rows = []
    jsonl_path = out_dir / "raw_results.jsonl"

    with open(jsonl_path, "w", encoding="utf-8") as jf:
        for item in QUESTIONS:
            qid = item["id"]
            q = item["question"]
            print(f"\n[{qid}/{len(QUESTIONS)}] {q}")
            print("-" * 80)

            print("Running Chroma...")
            chroma = safe_call(chroma_rag, q)
            print(f"Chroma ok={chroma['ok']} time={chroma['time_sec']:.3f}s chars={chroma['answer_chars']}")

            print("Running Neo4j...")
            neo4j = safe_call(neo4j_rag, q)
            print(f"Neo4j ok={neo4j['ok']} time={neo4j['time_sec']:.3f}s chars={neo4j['answer_chars']}")

            print("Judging...")
            judge = judge_answer(q, item["expected_winner"], chroma["answer"], neo4j["answer"])
            print(f"Winner={judge['winner']} ChromaScore={judge['chroma_score']} Neo4jScore={judge['neo4j_score']}")

            faster = "chroma" if chroma["time_sec"] < neo4j["time_sec"] else "neo4j"
            row = {
                "id": qid,
                "category": item["category"],
                "expected_winner": item["expected_winner"],
                "question": q,
                "chroma_ok": chroma["ok"],
                "chroma_time_sec": chroma["time_sec"],
                "chroma_answer_chars": chroma["answer_chars"],
                "chroma_error": chroma["error"],
                "chroma_answer": chroma["answer"],
                "neo4j_ok": neo4j["ok"],
                "neo4j_time_sec": neo4j["time_sec"],
                "neo4j_answer_chars": neo4j["answer_chars"],
                "neo4j_error": neo4j["error"],
                "neo4j_answer": neo4j["answer"],
                "faster_system": faster,
                "time_delta_sec": abs(chroma["time_sec"] - neo4j["time_sec"]),
                "judge_winner": judge["winner"],
                "expected_matched": judge["winner"] == item["expected_winner"],
                "chroma_score": judge["chroma_score"],
                "neo4j_score": judge["neo4j_score"],
                "judge_reason": judge["judge_reason"],
            }
            rows.append(row)
            jf.write(json.dumps({**row, "judge_raw": judge["judge_raw"]}, ensure_ascii=False) + "\n")
            jf.flush()

    csv_path = out_dir / "benchmark_results.csv"
    write_csv(csv_path, rows)

    summary = summarize(rows)
    summary_path = out_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    report_path = out_dir / "report.md"
    report_path.write_text(markdown_report(summary, rows), encoding="utf-8")

    print("\n" + "=" * 80)
    print("DONE")
    print(f"CSV:     {csv_path}")
    print(f"JSONL:   {jsonl_path}")
    print(f"Summary: {summary_path}")
    print(f"Report:  {report_path}")
    print("=" * 80)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()