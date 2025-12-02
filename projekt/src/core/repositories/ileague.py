"""A repository for league entity."""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.league import League, LeagueBroker, LeagueIn
from src.infrastructure.dto.leaguedto import LeagueDTO


class ILeagueRepository(ABC):
    """An abstract repository class for league."""

    @abstractmethod
    async def get_by_id(self, league_id: int) -> Any | None:
        """Get league by ID."""

    @abstractmethod
    async def get_all_public(self) -> Iterable[LeagueDTO]:
        """Get all public leagues."""
    
    @abstractmethod
    async def add_league(self, data: LeagueBroker) -> LeagueDTO | None:
        """Add a new league."""

    @abstractmethod
    async def update_league(
        self,
        league_id: int,
        data: LeagueBroker,
    ) -> Any | None:
        """Update league data."""

    @abstractmethod
    async def delete_league(self, league_id: int) -> bool:
        """Delete league from the data storage.

        Args:
            league_id (int): The id of the league.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_by_owner(self, owner_id: int) -> Iterable[LeagueDTO]:
        """Get all leagues owned by a user."""

    @abstractmethod
    async def archive_league(self, league_id: int) -> LeagueDTO | None:
        """Archive a league."""

    @abstractmethod
    async def get_all_archived(self) -> Iterable[LeagueDTO]:
        """Get all archived leagues."""

    @abstractmethod
    async def get_by_city(self, city: str) -> Any:
        """Get leagues by city."""