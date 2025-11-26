from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.match import Match, MatchIn


class IMatchRepository(ABC):
    """"""

    @abstractmethod
    async def get_match_by_id(self, match_id: int) -> Match | None:
        """"""

    
    @abstractmethod
    async def get_matches_by_league(self, league_id: int) -> Iterable[Any]:
        """"""


    @abstractmethod
    async def create_matches(self, data: MatchIn) -> Match | None:
        """"""

    @abstractmethod
    async def update_match(self, match: Match) -> Match | None:
        """"""

    
    @abstractmethod
    async def delete_match(self, match_id: int) -> bool:
        """The abstract updating removing match from the data storage.

        Args:
            match_id (int): The id of the match.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def update_score(self, match_id: int, home_score: int, away_score: int) -> Any | None:
        """Updates match score."""