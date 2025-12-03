from abc import ABC, abstractmethod
from typing import Iterable
from projekt.src.core.domain.match import Match,MatchIn

class IMatchService(ABC):
    """ """
    
    @abstractmethod
    async def add_match(self, match: MatchIn) -> Match | None:
        """ """
    
    @abstractmethod
    async def get_matches_by_league(self, league_id: int) -> Iterable[Match]:
        """ """
    @abstractmethod
    async def get_archived_matches(self) -> Iterable[Match]:
        """"""
    
    async def enter_result(
        self,
        match_id: int,
        home_score: int,
        away_score: int,
    ) -> Match | None:
        """"""

    @abstractmethod
    async def get_by_team(self, team_id: int) -> Match | None:
        """"""