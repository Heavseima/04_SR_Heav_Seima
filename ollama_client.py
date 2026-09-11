"""Call Ollama directly; no RAG framework or API key needed."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from config import OLLAMA_URL


def post(endpoint, payload):
    request = Request(f"{OLLAMA_URL}/api/{endpoint}",
                      data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=300) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Ollama error: {exc.read().decode()}. Check ollama list.") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError("Cannot reach Ollama. Start ollama serve and check OLLAMA_URL.") from exc
