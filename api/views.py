from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .analysis import ia, vt
from .models import (
    HttpAgentDecision,
)
from .utils.extract import extract_callback_url
from .utils.request import build_request_context


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

    context = build_request_context(request=request, callback_url=callback_url)

    ia(context=context)
    vt(context=context)

    return JsonResponse(dict(status="success"))
