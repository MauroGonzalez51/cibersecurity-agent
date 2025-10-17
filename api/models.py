import datetime
from typing import List, Literal

from pydantic import BaseModel, Field


class HttpAgentDecision(BaseModel):
    decision: Literal["ALLOW", "BLOCK"]
    error: str
    risk_score: float
    threats: List[str]
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    callback_url: str | None


if __name__ == "__main__":
    pass
