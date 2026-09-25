from config import settings
from graph.neo4j_client import run_cypher
from utils.llm import llm


def neo4j_rag(
    question: str,
    schema: str = None,
    intent_prompt: str = None,
    cypher_prompt: str = None,
    cypher_fix_prompt: str = None,
    answer_prompt: str = None,
    verbose: bool = True,
) -> dict:
    schema            = schema            or settings.NEO4J_SCHEMA
    intent_prompt     = intent_prompt     or settings.INTENT_PROMPT
    cypher_prompt     = cypher_prompt     or settings.CYPHER_PROMPT
    cypher_fix_prompt = cypher_fix_prompt or settings.CYPHER_FIX_PROMPT
    answer_prompt     = answer_prompt     or settings.NEO4J_ANSWER_PROMPT

    def _log(*args):
        if verbose:
            print(*args)

    _log(f"\n[neo4j_rag] Question: {question}")
    _log("-" * 50)

    intent = llm(intent_prompt.format(question=question))
    _log(f"Intent:\n{intent}\n")


    cypher = llm(cypher_prompt.format(
        schema=schema, intent=intent, question=question
    ))
    _log(f"Cypher:\n{cypher}\n")

    try:
        records = run_cypher(cypher)
    except Exception as e:
        _log(f"Error: {e} — asking LLM to fix …")
        cypher = llm(cypher_fix_prompt.format(cypher=cypher, error=e))
        _log(f"Fixed Cypher:\n{cypher}\n")
        try:
            records = run_cypher(cypher)
        except Exception as e2:
            _log(f"Failed again: {e2}")
            return {"intent": intent, "cypher": cypher, "records": [], "answer": str(e2)}

    _log(f"Records: {records}\n")

    
    answer = llm(answer_prompt.format(question=question, records=records))
    _log(f"Answer: {answer}")

    return {"intent": intent, "cypher": cypher, "records": records, "answer": answer}
