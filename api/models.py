import datetime
import enum
from typing import Any, Dict, List, Literal

from django.db import models
from pydantic import BaseModel, Field


class CountryRiskRecord(models.Model):
    country_code = models.CharField(max_length=2, unique=True)
    total_requests = models.IntegerField(default=0)
    malicious_requests = models.IntegerField(default=0)
    risk_score = models.FloatField(default=0.0)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["country_code"]),
        ]

    def __str__(self):
        return f"{self.country_code} (risk: {self.risk_score:.2f})"


class IpRiskRecord(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)
    total_requests = models.IntegerField(default=0)
    malicious_requests = models.IntegerField(default=0)
    risk_score = models.FloatField(default=0.0)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address"]),
        ]

    def __str__(self):
        return f"{self.ip_address} (risk: {self.risk_score:.2f})"


class Fields(enum.Enum):
    Unknown = "UNKNOWN"


class HttpAgentRequestContextParsedUrl(BaseModel):
    scheme: str
    netloc: str
    domain: str
    port: int | None
    path: str
    query: str
    fragment: str
    params: Dict[str, List[str]]


class HttpAgentRequestContext(BaseModel):
    callback_url: str
    parsed_url: HttpAgentRequestContextParsedUrl
    method: str | None
    headers: Dict[str, Any]
    body: bytes
    content_type: str | None
    client_ip: str
    user_agent: str
    query_params: Dict[str, Any]
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )


class HttpAgentDecision(BaseModel):
    decision: Literal["ALLOW", "BLOCK"]
    risk_score: float
    threats: List[str]
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    callback_url: str | None
    context: HttpAgentRequestContext | None


class HttpAgentAIDecision(BaseModel):
    decision: Literal["ALLOW", "BLOCK"]
    risk_score: float
    threats: List[str]
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    callback_url: str | None
    summary: str
    recommendations: List[str]


class HttpAgentVTResponse(BaseModel):
    attributes: Dict[str, Any]
    stats: Dict[str, Any]
    reputation: int = Field(default_factory=lambda: 0)
    country: str
    asn: int
    network: str


class HttpAgentGeoResponse(BaseModel):
    country_code: str | None
    country_name: str | None
    city_name: str | None
    lat: float | None
    lon: float | None


if __name__ == "__main__":
    pass
