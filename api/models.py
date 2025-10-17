import datetime
import enum
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field


class Fields(enum.Enum):
    Unknown = "UNKNOWN"


class HttpAgentDecision(BaseModel):
    decision: Literal["ALLOW", "BLOCK"]
    error: str
    risk_score: float
    threats: List[str]
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    callback_url: str | None


class HttpAgentAIDecision(HttpAgentDecision):
    summary: str
    recommendations: List[str]


class HttpAgentVTResponse(BaseModel):
    attributes: Dict[str, Any]
    stats: Dict[str, Any]
    reputation: int = Field(default_factory=lambda: 0)
    country: str
    asn: int
    network: str


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


if __name__ == "__main__":
    pass
