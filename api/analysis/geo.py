import geoip2.database
from django.db import models, transaction

from core.env import env_config

from ..models import CountryRiskRecord, HttpAgentGeoResponse, HttpAgentRequestContext

reader = geoip2.database.Reader(rf"{env_config.geoip_database_path.absolute()}")


def geo(context: HttpAgentRequestContext) -> HttpAgentGeoResponse | None:
    ip = context.client_ip

    try:
        record = reader.city(ip)
        country_code, country_name, city_name, lat, lon = (
            record.country.iso_code,
            record.country.name,
            record.city.name,
            record.location.latitude,
            record.location.longitude,
        )
    except Exception:
        return

    with transaction.atomic():
        obj, created = CountryRiskRecord.objects.select_for_update().get_or_create(
            country_code=country_code,
            defaults=dict(total_requests=1, malicious_requests=0, risk_score=0.0),
        )

        if not created:
            obj.total_requests = models.F("total_requests") + 1
            obj.save()

    return HttpAgentGeoResponse(
        country_code=country_code,
        country_name=country_name,
        city_name=city_name,
        lat=lat,
        lon=lon,
    )


if __name__ == "__main__":
    pass
