"""A repository for league entity."""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.league import League, LeagueBroker, LeagueIn
from src.infrastructure.dto.leaguedto import LeagueDTO


class ILeagueRepository(ABC):
    """An abstract repository class for league."""

    @abstractmethod
    async def get_by_id(self, league_id: int) -> Any | None:
        """Get league by ID.

        Args:
            league_id (int): The ID of the league.

        Returns:
            Any | None: The league object if exists.
        """

    @abstractmethod
    async def get_all_public(self) -> Iterable[LeagueDTO]:
        """Get all public leagues.

        Returns:
            Iterable[LeagueDTO]: The collection of all public leagues.
        """
    
    @abstractmethod
    async def add_league(self, data: LeagueBroker) -> LeagueDTO | None:
        """Add a new league.

        Args:
            data (LeagueBroker): The league input data with owner ID.

        Returns:
            LeagueDTO | None: The created league object.
        """

    @abstractmethod
    async def update_league(
        self,
        league_id: int,
        data: LeagueBroker,
    ) -> Any | None:
        """Update league data.

        Args:
            league_id (int): The ID of the league.
            data (LeagueBroker): The updated league details.

        Returns:
            Any | None: The updated league object.
        """

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
        """Get all leagues owned by a user.

        Args:
            owner_id (int): The ID of the owner.

        Returns:
            Iterable[LeagueDTO]: The collection of leagues owned by the user.
        """

    @abstractmethod
    async def archive_league(self, league_id: int) -> LeagueDTO | None:
        """Archive a league.

        Args:
            league_id (int): The ID of the league.

        Returns:
            LeagueDTO | None: The archived league object.
        """

    @abstractmethod
    async def get_all_archived(self) -> Iterable[LeagueDTO]:
        """Get all archived leagues.

        Returns:
            Iterable[LeagueDTO]: The collection of all archived leagues.
        """

    @abstractmethod
    async def get_by_city(self, city: str) -> Any:
        """Get leagues by city.

        Args:
            city (str): The name of the city.

        Returns:
            Any: The collection of leagues in the city.
        """