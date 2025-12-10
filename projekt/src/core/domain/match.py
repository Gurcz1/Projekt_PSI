"""A model containing match-related models."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    PENDING = "pending"
    FINISHED = "finished"


class MatchIn(BaseModel):
    """An input match model."""
    league_id: int
    home_team_id: int
    away_team_id: int
    date: str


class MatchUpdateIn(BaseModel):
    """Model for updating match score and date."""
    home_score: int | None = None
    away_score: int | None = None
    date: str | None = None


class MatchBroker(MatchIn):
    """A broker class including user in the model."""
    submitted_by: int | None = None


class Match(MatchBroker):
    """The match model class."""
    id: int
    home_score: int | None = None
    away_score: int | None = None
    status: str | None = "scheduled"

    model_config = ConfigDict(from_attributes=True, extra='ignore')