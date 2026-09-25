
import requests
from config import settings


def llm(prompt: str, model_url: str = None, model_id: str = None) -> str:
    url = (model_url or settings.MODEL_URL) + "/api/generate"
    mid = model_id or settings.MODEL_ID

    response = requests.post(
        url,
        json={"model": mid, "prompt": prompt, "stream": False},
    )
    response.raise_for_status()
    return response.json().get("response", "No response").strip()
