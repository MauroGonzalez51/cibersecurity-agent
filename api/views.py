from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .analysis import geo, ia, reasoning, vt
from .models import HttpAgentDecision
from .utils.extract import extract_callback_url
from .utils.request import build_request_context


@csrf_exempt
def agent(request: HttpRequest):
    callback_url = extract_callback_url(request=request)

    if not callback_url:
        return JsonResponse(
            HttpAgentDecision(
                decision="BLOCK",
                risk_score=100,
                threats=["missing_target_url"],
                callback_url=callback_url,
                context=None,
            )
        )

    context = build_request_context(request=request, callback_url=callback_url)

    _ia, _vt, _geo = (
        ia(context=context),
        vt(context=context),
        geo(context=context),
    )

    decision = reasoning(context=context, vt=_vt, ia=_ia, geo=_geo)

    # TODO: based on the decision, notify the user of it

    return JsonResponse(decision.model_dump_json(indent=4))
