"""A module containing team related DTOs."""

from uuid import UUID
from pydantic import BaseModel, ConfigDict

class TeamDTO(BaseModel):
    """A team DTO model."""
    id: UUID
    name: str
    league_id: UUID
    captain_id: UUID

    model_config = ConfigDict(from_attributes=True, extra="ignore")
