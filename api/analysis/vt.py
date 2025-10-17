from typing import Any, Dict

import httpx

from core.env import env_config

from ..models import Fields, HttpAgentRequestContext, HttpAgentVTResponse


def vt(context: HttpAgentRequestContext):
    if not env_config.virustotal_api_key:
        return

    with httpx.Client(timeout=60) as client:
        response = client.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{context.client_ip}",
            headers={"x-apikey": env_config.virustotal_api_key},
        )

        if not response.status_code == 200:
            return

        data = response.json()
        attributes: Dict[str, Any] = data.get("data", {}).get("attributes", {})

        return HttpAgentVTResponse(
            attributes=attributes,
            stats=attributes.get("last_analysis_stats", {}),
            reputation=attributes.get("reputation", 0),
            country=attributes.get("country", str(Fields.Unknown)),
            asn=attributes.get("asn", 0),
            network=attributes.get("network", str(Fields.Unknown)),
        )


if __name__ == "__main__":
    pass
