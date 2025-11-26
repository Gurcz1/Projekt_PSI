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
    team_a_id: int
    team_b_id: int
    match_date: datetime


class Match(MatchIn):
    """The match model class."""
    id: int
    home_score: int | None = None
    away_score: int | None = None
    status: MatchStatus = MatchStatus.SCHEDULED

    model_config = ConfigDict(from_attributes=True, extra='ignore')