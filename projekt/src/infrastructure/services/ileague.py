"""Module containing league service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.league import League, LeagueIn, LeagueBroker
from src.infrastructure.dto.leaguedto import LeagueDTO


class ILeagueService(ABC):
    """An abstract class representing protocol of league service."""

    @abstractmethod
    async def get_public_leagues(self) -> Iterable[LeagueDTO]:
        """The abstract getting public leagues from the repository.

        Returns:
            Iterable[LeagueDTO]: The collection of the all public leagues.
        """

    @abstractmethod
    async def get_by_id(self, league_id: int) -> LeagueDTO | None:
        """The abstract getting a league from the repository.

        Args:
            league_id (int): The id of the league.

        Returns:
            LeagueDTO | None: The league data if exists.
        """

    @abstractmethod
    async def add_league(self, data: LeagueBroker) -> LeagueDTO | None:
        """The abstract adding new league to the repository.

        Args:
            data (LeagueBroker): The attributes of the league with owner.

        Returns:
            LeagueDTO | None: The created league.
        """

    @abstractmethod
    async def update_league(
        self,
        league_id: int,
        data: LeagueBroker,
        user_id: int,
    ) -> LeagueDTO | None:
        """The abstract updating league data in the repository.

        Args:
            league_id (int): The league id.
            data (LeagueBroker): The attributes of the league.

        Returns:
            League | None: The updated league.
        """

    @abstractmethod
    async def delete_league(self, league_id: int, user_id: int) -> bool:
        """The abstract removing league from the repository.

        Args:
            league_id (int): The league id.
            user_id (int): The user requesting deletion.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_my_leagues(self, user_id: int) -> Iterable[LeagueDTO]:
        """Get leagues owned by user."""

    @abstractmethod
    async def archive_league(self, league_id: int) -> LeagueDTO | None:
        """Archive a league."""

    @abstractmethod
    async def get_leagues_by_city(self, city: str) -> Iterable[LeagueDTO]:
        """Get leagues by city."""

    @abstractmethod
    async def get_archived_leagues(self) -> Iterable[LeagueDTO]:
        """Get all archived leagues."""
        
    @abstractmethod
    async def get_standings(self, league_id: int) -> Iterable[Any]:
        """Get league standings"""

    @abstractmethod
    async def generate_scheudle(self, league_id: int, user_id: int) -> Iterable[Any]:
        """Generate league scheudle"""