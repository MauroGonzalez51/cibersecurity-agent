from typing import List, Optional

from django.db import transaction

from ..models import (
    CountryRiskRecord,
    HttpAgentAIDecision,
    HttpAgentDecision,
    HttpAgentGeoResponse,
    HttpAgentRequestContext,
    HttpAgentVTResponse,
    IpRiskRecord,
)

IA_WEIGHT = 25
VT_WEIGHT = 30
GEO_WEIGHT = 20
LOOKBACK_WEIGHT = 25


def reasoning(
    context: HttpAgentRequestContext,
    ia: Optional[HttpAgentAIDecision],
    vt: Optional[HttpAgentVTResponse],
    geo: Optional[HttpAgentGeoResponse],
):
    risk_score: float = 0.0
    threats: List[str] = []

    if ia is None:
        risk_score += IA_WEIGHT
        threats.append("missing:ia")
    else:
        normalized_ia = (ia.risk_score / 100) * IA_WEIGHT
        risk_score += min(normalized_ia, IA_WEIGHT)
        threats += ia.threats

    if vt is None:
        risk_score += 40
        threats.append("missing:vt")
    else:
        normalized_vt = (abs(vt.reputation or 0) / 100) * VT_WEIGHT
        risk_score += min(normalized_vt, VT_WEIGHT)

    if geo is None:
        risk_score += 20
        threats.append("missing:geo")
    else:
        country, _ = CountryRiskRecord.objects.select_for_update().get_or_create(
            country_code=geo.country_code,
            defaults=dict(total_requests=1, malicious_requests=0, risk_score=0.0),
        )

        if not country._state.adding:
            country.total_requests = country.total_requests + 1

        if country.total_requests > 0:
            risk_score += min(
                (country.malicious_requests / country.total_requests) * GEO_WEIGHT,
                GEO_WEIGHT,
            )

    lookback, _ = IpRiskRecord.objects.select_for_update().get_or_create(
        ip_address=context.client_ip,
        defaults=dict(total_requests=1, malicious_requests=0, risk_score=0.0),
    )

    risk_score += min(
        (lookback.malicious_requests / lookback.total_requests) * LOOKBACK_WEIGHT,
        LOOKBACK_WEIGHT,
    )

    risk_score = min(risk_score, 100)

    decision = HttpAgentDecision(
        decision="BLOCK" if risk_score >= 50 else "ALLOW",
        risk_score=risk_score,
        threats=threats,
        callback_url=context.callback_url,
        context=context,
    )

    if decision.decision == "BLOCK":
        with transaction.atomic():
            if geo:
                record = CountryRiskRecord.objects.filter(
                    country_code=geo.country_code
                ).first()

                if record:
                    record.malicious_requests = record.malicious_requests + 1
                    record.save()

        with transaction.atomic():
            record = IpRiskRecord.objects.filter(ip_address=context.client_ip).first()

            if record:
                record.malicious_requests = record.malicious_requests + 1
                record.save()

    return decision


if __name__ == "__main__":
    pass
