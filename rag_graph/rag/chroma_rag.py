
from config import settings
from vector.chroma_index import get_collection, query_collection
from utils.llm import llm


def chroma_rag(
    question: str,
    n_results: int = 5,
    collection=None,
    intent_prompt: str = None,
    search_query_prompt: str = None,
    answer_prompt: str = None,
    verbose: bool = True,
) -> dict:

    intent_prompt       = intent_prompt       or settings.INTENT_PROMPT
    search_query_prompt = search_query_prompt or settings.SEARCH_QUERY_PROMPT
    answer_prompt       = answer_prompt       or settings.CHROMA_ANSWER_PROMPT
    collection          = collection          or get_collection()

    def _log(*args):
        if verbose:
            print(*args)

    _log(f"\n[chroma_rag] Question: {question}")
    _log("-" * 50)

    intent = llm(intent_prompt.format(question=question))
    _log(f"Intent:\n{intent}\n")

    search_query = llm(search_query_prompt.format(
        intent=intent, question=question
    ))
    _log(f"Search query: {search_query}\n")

    try:
        titles, documents = query_collection(search_query, n_results, collection)
    except Exception as e:
        _log(f"Chroma query failed: {e}")
        return {"intent": intent, "search_query": search_query, "titles": [], "answer": str(e)}

    _log(f"Retrieved: {titles}\n")

    context = "\n\n".join(
        f"Movie: {t}\n{d}" for t, d in zip(titles, documents)
    )
    
    answer = llm(answer_prompt.format(context=context, question=question))
    _log(f"Answer: {answer}")

    return {"intent": intent, "search_query": search_query, "titles": titles, "answer": answer}
