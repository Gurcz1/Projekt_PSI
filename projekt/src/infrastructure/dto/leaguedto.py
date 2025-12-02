"""A module containing league related DTOs."""

from typing import Any
from pydantic import BaseModel, ConfigDict
from src.core.domain.league import SportType, LeagueStatus
from src.infrastructure.dto.userdto import UserDTO


class LeagueDTO(BaseModel):
    """A model representing DTO for league data."""
    id: int
    name: str
    city: str
    sport_type: SportType
    is_private: bool
    owner: UserDTO
    status: LeagueStatus

    model_config = ConfigDict(
        from_attributes=True, 
        extra="ignore",
        arbitrary_types_allowed=True,)

    @classmethod
    def from_record(cls, record: Any) -> "LeagueDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            LeagueDTO: The final DTO instance.
        """
        record_dict = dict(record)
        
        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            city=record_dict.get("city"),  # type: ignore
            sport_type=record_dict.get("sport_type"),  # type: ignore
            is_private=record_dict.get("is_private"),  # type: ignore
            status=record_dict.get("status"),  # type: ignore
            owner=UserDTO(
                id=record_dict.get("id_1"),  # type: ignore
                email=record_dict.get("email"),  # type: ignore
            ),
        )
