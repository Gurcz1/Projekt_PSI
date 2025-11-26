"""A model containing league-related models."""

from pydantic import BaseModel, ConfigDict, UUID1
from enum import Enum


class SportType(str, Enum):
    FOOTBALL = "football"
    VOLLEYBALL = "volleyball"
    BASKETBALL = "basketball"
    HANDBALL = "handball"
    OTHER = "other"


class LeagueStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class LeagueIn(BaseModel):
    """An input league model."""
    name: str
    city: str
    sport_type: SportType
    is_private: bool = False


class LeagueBroker(LeagueIn):
    """A broker class including admin in the model."""
    admin_id: UUID1


class League(LeagueBroker):
    """The league model class."""
    id: int
    status: LeagueStatus = LeagueStatus.ACTIVE

    model_config = ConfigDict(from_attributes=True, extra="ignore")



