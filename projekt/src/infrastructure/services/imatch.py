"""A repository for a match service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.match import Match, MatchBroker, MatchUpdateIn

class IMatchService(ABC):
    """An abstract repository class for match."""

    @abstractmethod
    async def get_match_by_id(self, match_id: int) -> Match | None:
        """Get match by ID."""

    @abstractmethod
    async def get_all_matches(self) -> Iterable[Match]:
        """Get all matches."""

    @abstractmethod
    async def get_matches_by_league(self, league_id: int) -> Iterable[Match]:
        """Get all matches in a league."""

    @abstractmethod
    async def get_matches_by_team(self, team_id: int) -> Iterable[Match]:
        """Get all matches for a team (home or away)."""

    @abstractmethod
    async def create_match(self, data: MatchBroker) -> Match | None:
        """Create a new match."""

    @abstractmethod
    async def update_match(self, match_id: int, data: MatchUpdateIn) -> Match | None:
        """Update match score and/or date."""

    @abstractmethod
    async def delete_match(self, match_id: int) -> bool:
        """Delete a match."""

