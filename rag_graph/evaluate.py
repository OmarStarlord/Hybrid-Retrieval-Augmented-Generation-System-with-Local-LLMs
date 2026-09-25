import time
import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag.chroma_rag import chroma_rag
from rag.neo4j_rag import neo4j_rag


EVALUATION_DATASET = [
    {
        "question": "Which directors have directed more than one movie?",
        "ground_truth": "The answer should list directors who are connected to more than one movie through DIRECTED relationships."
    },
    {
        "question": "Which actors have appeared in more than one movie?",
        "ground_truth": "The answer should list actors who are connected to more than one movie through ACTED_IN relationships."
    },
    {
        "question": "Which movies are in the Action genre?",
        "ground_truth": "The answer should list movies connected to the Genre node named Action."
    },
    {
        "question": "Which movies are in the Science Fiction genre?",
        "ground_truth": "The answer should list movies connected to the Genre node named Science Fiction."
    },
    {
        "question": "Which movies are in the Horror genre?",
        "ground_truth": "The answer should list movies connected to the Genre node named Horror."
    },
    {
        "question": "Which movies are both Action and Science Fiction?",
        "ground_truth": "The answer should list movies connected to both the Action and Science Fiction genre nodes."
    },
    {
        "question": "Which movies are both Action and Adventure?",
        "ground_truth": "The answer should list movies connected to both the Action and Adventure genre nodes."
    },
    {
        "question": "Which movies are both Horror and Thriller?",
        "ground_truth": "The answer should list movies connected to both the Horror and Thriller genre nodes."
    },
    {
        "question": "What genres does Mortal Kombat belong to?",
        "ground_truth": "The answer should list the genres connected to the movie Mortal Kombat through HAS_GENRE relationships."
    },
    {
        "question": "Who acted in Mortal Kombat?",
        "ground_truth": "The answer should list people connected to Mortal Kombat through ACTED_IN relationships."
    },
    {
        "question": "Who directed Mortal Kombat?",
        "ground_truth": "The answer should list people connected to Mortal Kombat through DIRECTED relationships."
    },
    {
        "question": "What keywords are associated with Mortal Kombat?",
        "ground_truth": "The answer should list keywords connected to Mortal Kombat through HAS_KEYWORD relationships."
    },
    {
        "question": "Which movies share actors with Mortal Kombat?",
        "ground_truth": "The answer should list other movies connected to the same actors who acted in Mortal Kombat."
    },
    {
        "question": "Which movies share genres with Mortal Kombat?",
        "ground_truth": "The answer should list movies connected to genres that are also connected to Mortal Kombat."
    },
    {
        "question": "Which movies share keywords with Mortal Kombat?",
        "ground_truth": "The answer should list movies connected to keywords that are also connected to Mortal Kombat."
    },
    {
        "question": "What genres does Avatar: Fire and Ash belong to?",
        "ground_truth": "The answer should list genres connected to Avatar: Fire and Ash through HAS_GENRE relationships."
    },
    {
        "question": "Who acted in Avatar: Fire and Ash?",
        "ground_truth": "The answer should list people connected to Avatar: Fire and Ash through ACTED_IN relationships."
    },
    {
        "question": "Who directed Avatar: Fire and Ash?",
        "ground_truth": "The answer should list people connected to Avatar: Fire and Ash through DIRECTED relationships."
    },
    {
        "question": "Which movies share genres with Avatar: Fire and Ash?",
        "ground_truth": "The answer should list movies connected to the same genres as Avatar: Fire and Ash."
    },
    {
        "question": "Which movies have the keyword revenge?",
        "ground_truth": "The answer should list movies connected to the Keyword node named revenge."
    },
    {
        "question": "Which movies have the keyword martial arts?",
        "ground_truth": "The answer should list movies connected to the Keyword node named martial arts."
    },
    {
        "question": "Which movies have the keyword based on video game?",
        "ground_truth": "The answer should list movies connected to the Keyword node named based on video game."
    },
    {
        "question": "Which people both directed and acted in movies?",
        "ground_truth": "The answer should list people who have at least one DIRECTED relationship and at least one ACTED_IN relationship."
    },
    {
        "question": "Which movie has the most keywords?",
        "ground_truth": "The answer should return the movie or movies with the highest number of HAS_KEYWORD relationships."
    },
    {
        "question": "Which genre has the most movies?",
        "ground_truth": "The answer should return the genre connected to the largest number of movies through HAS_GENRE relationships."
    }
]

print("Loading sentence-transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")


def calculate_similarity_score(generated_answer, ground_truth_answer):
    """Calculate semantic similarity between generated answer and ground truth."""
    if not generated_answer or not ground_truth_answer:
        return 0.0

    embedding1 = model.encode(generated_answer, convert_to_tensor=True)
    embedding2 = model.encode(ground_truth_answer, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embedding1, embedding2)
    score = cosine_scores.item()
    return max(0, min(1, score))


def create_visualizations(df):
    """Generate and save evaluation plots."""
    os.makedirs("evaluation_results", exist_ok=True)
    sns.set_theme(style="whitegrid")

    latency_df = df[["chroma_latency", "neo4j_latency"]].rename(
        columns={
            "chroma_latency": "Chroma RAG",
            "neo4j_latency": "Neo4j GraphRAG"
        }
    )

    accuracy_df = df[["chroma_accuracy", "neo4j_accuracy"]].rename(
        columns={
            "chroma_accuracy": "Chroma RAG",
            "neo4j_accuracy": "Neo4j GraphRAG"
        }
    )

    plt.figure(figsize=(10, 6))
    latency_df.mean().plot(kind="bar", color=["skyblue", "lightgreen"])
    plt.title("Average Query Latency")
    plt.ylabel("Latency Seconds")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("evaluation_results/average_latency.png")
    print("Saved evaluation_results/average_latency.png")

    plt.figure(figsize=(10, 6))
    accuracy_df.mean().plot(kind="bar", color=["skyblue", "lightgreen"])
    plt.title("Average Semantic Accuracy")
    plt.ylabel("Semantic Similarity Score")
    plt.xticks(rotation=0)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig("evaluation_results/average_accuracy.png")
    print("Saved evaluation_results/average_accuracy.png")

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=latency_df)
    plt.title("Latency Distribution")
    plt.ylabel("Latency Seconds")
    plt.tight_layout()
    plt.savefig("evaluation_results/latency_distribution.png")
    print("Saved evaluation_results/latency_distribution.png")

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=accuracy_df)
    plt.title("Semantic Accuracy Distribution")
    plt.ylabel("Semantic Similarity Score")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig("evaluation_results/accuracy_distribution.png")
    print("Saved evaluation_results/accuracy_distribution.png")

    plt.close("all")


def run_evaluation():
    results = []

    print(f"Starting evaluation with {len(EVALUATION_DATASET)} questions...")

    for i, item in enumerate(EVALUATION_DATASET, start=1):
        question = item["question"]
        ground_truth = item["ground_truth"]

        print(f"\n[{i}/{len(EVALUATION_DATASET)}] Testing question: {question}")

        # Chroma RAG
        try:
            start_time = time.time()
            chroma_result = chroma_rag(question, verbose=False)
            chroma_latency = time.time() - start_time
            chroma_answer = chroma_result.get("answer", "") if isinstance(chroma_result, dict) else str(chroma_result)
            chroma_accuracy = calculate_similarity_score(chroma_answer, ground_truth)
        except Exception as e:
            chroma_latency = 0.0
            chroma_answer = f"ERROR: {e}"
            chroma_accuracy = 0.0

        # Neo4j GraphRAG
        try:
            start_time = time.time()
            neo4j_result = neo4j_rag(question, verbose=False)
            neo4j_latency = time.time() - start_time
            neo4j_answer = neo4j_result.get("answer", "") if isinstance(neo4j_result, dict) else str(neo4j_result)
            neo4j_accuracy = calculate_similarity_score(neo4j_answer, ground_truth)
        except Exception as e:
            neo4j_latency = 0.0
            neo4j_answer = f"ERROR: {e}"
            neo4j_accuracy = 0.0

        results.append({
            "question": question,
            "ground_truth": ground_truth,
            "chroma_answer": chroma_answer,
            "neo4j_answer": neo4j_answer,
            "chroma_latency": chroma_latency,
            "neo4j_latency": neo4j_latency,
            "chroma_accuracy": chroma_accuracy,
            "neo4j_accuracy": neo4j_accuracy,
        })

        print(f"  Chroma | Accuracy: {chroma_accuracy:.2f} | Latency: {chroma_latency:.2f}s")
        print(f"  Neo4j  | Accuracy: {neo4j_accuracy:.2f} | Latency: {neo4j_latency:.2f}s")
        print(f"  Chroma answer: {chroma_answer[:250]}{'...' if len(chroma_answer) > 250 else ''}")
        print(f"  Neo4j answer:  {neo4j_answer[:250]}{'...' if len(neo4j_answer) > 250 else ''}")

    if not results:
        print("No results generated.")
        return

    os.makedirs("evaluation_results", exist_ok=True)
    results_df = pd.DataFrame(results)
    results_df.to_csv("evaluation_results/evaluation_results.csv", index=False, encoding="utf-8")
    print("\nSaved raw evaluation data to evaluation_results/evaluation_results.csv")

    summary = {
        "chroma_avg_latency": results_df["chroma_latency"].mean(),
        "neo4j_avg_latency": results_df["neo4j_latency"].mean(),
        "chroma_avg_accuracy": results_df["chroma_accuracy"].mean(),
        "neo4j_avg_accuracy": results_df["neo4j_accuracy"].mean(),
    }

    print("\n=== Evaluation Summary ===")
    print(f"Chroma average latency: {summary['chroma_avg_latency']:.2f}s")
    print(f"Neo4j average latency:  {summary['neo4j_avg_latency']:.2f}s")
    print(f"Chroma average accuracy: {summary['chroma_avg_accuracy']:.2f}")
    print(f"Neo4j average accuracy:  {summary['neo4j_avg_accuracy']:.2f}")

    create_visualizations(results_df)
    print("\nEvaluation complete. Results saved in the evaluation_results directory.")


if __name__ == "__main__":
    run_evaluation()