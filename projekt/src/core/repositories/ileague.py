"""A repository for user entity."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.league import League, LeagueBroker, LeagueIn


class ILeagueRepository(ABC):


    @abstractmethod
    async def get_league_by_id(self, league_id: int) -> League | None:
        """ """


    @abstractmethod
    async def get_all_leagues(self) -> Iterable[League]:
        """ """
    

    @abstractmethod
    async def create_league(self, data: LeagueBroker) -> League | None:
        """"""


    @abstractmethod
    async def update_league(
        self,
        league_id: int,
        data: LeagueIn,
    ) -> League | None:
        """ """

    @abstractmethod
    async def delete_league(self, league_id: int) -> bool:
        """The abstract updating removing league from the data storage.

        Args:
            league_id (int): The id of the league.

        Returns:
            bool: Success of the operation.
        """