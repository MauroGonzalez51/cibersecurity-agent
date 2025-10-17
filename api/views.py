"""
Django HTTP Proxy View - Modernizado y refactorizado
Basado en django-revproxy, actualizado con httpx, tipado y mejor estructura.
"""

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import HttpAgentDecision
from .utils.extract import extract_callback_url


@csrf_exempt
def agent(request: HttpRequest):
    callback_url = extract_callback_url(request=request)

    if not callback_url:
        return JsonResponse(
            HttpAgentDecision(
                decision="BLOCK",
                error="missing callback url",
                risk_score=100,
                threats=["missing_target_url"],
                callback_url=callback_url,
            )
        )

    return JsonResponse(dict(status="success"))
