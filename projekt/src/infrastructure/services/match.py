<<<<<<< HEAD
from typing import Iterable

from projekt.src.core.domain.match import Match, MatchIn
from projekt.src.core.repositories.imatch import IMatchRepository
from projekt.src.infrastructure.services.imatch import IMatchService

class MatchService(IMatchService):
    
    _repository = IMatchRepository
    
    
    def __init__(self, repository: IMatchRepository) -> None:
        
        self._repository = repository
        
=======
"""A service for match entity."""

from typing import Any, Iterable

from src.core.domain.match import Match, MatchBroker, MatchUpdateIn
from src.core.repositories.imatch import IMatchRepository
from src.infrastructure.services.imatch import IMatchService


class MatchService(IMatchService):
    """A service for match entity."""

    def __init__(self, repository: IMatchRepository):
        """The initializer of the `match service`.

        Args:
            repository (IMatchRepository): The reference to the repository.
        """
        self.repository = repository

    async def get_match_by_id(self, match_id: int) -> Any | None:
        """The method getting match by ID."""

        return await self.repository.get_match_by_id(match_id)

    async def get_all_matches(self) -> Iterable[Any]:
        """The method getting all matches."""

        return await self.repository.get_all_matches()

    async def get_matches_by_league(self, league_id: int) -> Iterable[Any]:
        """The method getting all matches by league ID."""

        return await self.repository.get_matches_by_league(league_id)

    async def get_matches_by_team(self, team_id: int) -> Iterable[Any]:
        """The method getting all matches by team ID (home or away)."""

        return await self.repository.get_matches_by_team(team_id)

    async def create_match(self, data: MatchBroker) -> Any | None:
        """Create a new match."""

        return await self.repository.create_match(data)

    async def update_match(self, match_id: int, data: MatchUpdateIn) -> Match | None:
        """Update match score and/or date."""

        return await self.repository.update_match(match_id, data)

    async def delete_match(self, match_id: int) -> bool:
        """The method deleting a match from the data storage."""

        return await self.repository.delete_match(match_id)
>>>>>>> 1b531bd07331be965cc9d6b99d045f24c7cab3b2
