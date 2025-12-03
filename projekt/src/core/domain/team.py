from pydantic import BaseModel, ConfigDict, UUID1


class TeamIn(BaseModel):
    """An input match model."""
    name: str
    league_id: int


class TeamBroker(TeamIn):
    """A broker class including user in the model."""
    captain_id: int


class Team(TeamBroker):
    """The team model class."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")