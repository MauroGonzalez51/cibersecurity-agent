from urllib.parse import parse_qs, urlparse

from django.http.request import HttpRequest

from ..models import HttpAgentRequestContext, HttpAgentRequestContextParsedUrl


def build_request_context(
    request: HttpRequest, callback_url: str
) -> HttpAgentRequestContext:
    """
    Construye el contexto completo de la petición para análisis.
    """
    parsed_url = urlparse(callback_url)

    domain = parsed_url.netloc.split(":")[0]

    port = None
    if ":" in parsed_url.netloc:
        try:
            port = int(parsed_url.netloc.split(":")[1])
        except ValueError:
            pass

    return HttpAgentRequestContext(
        callback_url=callback_url,
        parsed_url=HttpAgentRequestContextParsedUrl(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            domain=domain,
            port=port,
            path=parsed_url.path,
            query=parsed_url.query,
            fragment=parsed_url.fragment,
            params=parse_qs(parsed_url.query),
        ),
        method=request.method,
        headers=dict(request.headers),
        body=request.body,
        content_type=request.content_type,
        client_ip=_get_client_ip(request=request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        query_params=dict(request.GET),
    )


def _get_client_ip(request: HttpRequest) -> str:
    """Obtiene la IP real del cliente considerando proxies."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "unknown")
    return ip
