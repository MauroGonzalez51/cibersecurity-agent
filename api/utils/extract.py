import json
from typing import Optional

from django.http.request import HttpRequest


def extract_callback_url(request: HttpRequest) -> Optional[str]:
    """
    Extrae el callback_url de diferentes fuentes.

    Prioridad:
    1. Query parameter (?callback_url=...)
    2. Header (X-Callback-Url)
    3. Body JSON ({"callback_url": "..."})
    """
    # Query params
    callback_url = request.GET.get("callback_url")
    if callback_url:
        return callback_url

    # Headers
    callback_url = request.headers.get("X-Callback-Url")
    if callback_url:
        return callback_url

    # Body JSON
    if request.content_type == "application/json" and request.body:
        try:
            body = json.loads(request.body.decode())
            callback_url = body.get("callback_url")
            if callback_url:
                return callback_url
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    return None


if __name__ == "__main__":
    pass
