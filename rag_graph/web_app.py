import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from rag.chroma_rag import chroma_rag
from rag.neo4j_rag import neo4j_rag

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    chroma_result = chroma_rag(question, verbose=False)
    neo4j_result  = neo4j_rag(question,  verbose=False)

    return jsonify({
        "chroma_answer": chroma_result["answer"],
        "neo4j_answer":  neo4j_result["answer"],
        "cypher":        neo4j_result.get("cypher", ""),
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)