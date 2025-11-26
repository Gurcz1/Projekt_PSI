"""Module containing airport service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.league import League, LeagueIn


class ILeagueService(ABC):
    """An abstract class representing protocol of league repository."""

    @abstractmethod
    async def get_all_leagues(self) -> Iterable[League]:
        """The abstract getting all leagues from the repository.

        Returns:
            Iterable[league]: The collection of the all leagues.
        """

    @abstractmethod
    async def get_league_by_id(self, league_id: int) -> League | None:
        """The abstract getting a league from the repository.

        Args:
            league_id (int): The id of the league.

        Returns:
            league | None: The league data if exists.
        """

    @abstractmethod
    async def add_league(self, data: LeagueIn) -> None:
        """The abstract adding new league to the repository.

        Args:
            data (LeagueIn): The attributes of the league.
        """
    @abstractmethod
    async def update_league(
        self,
        league_id: int,
        data: LeagueIn,
    ) -> League | None:
        """The abstract updating league data in the repository.

        Args:
            league_id (int): The league id.
            data (leagueIn): The attributes of the league.

        Returns:
            League | None: The updated league.
        """

    @abstractmethod
    async def delete_league(self, league_id: int) -> bool:
        """The abstract updating removing league from the repository.

        Args:
            league_id (int): The league id.

        Returns:
            bool: Success of the operation.
        """