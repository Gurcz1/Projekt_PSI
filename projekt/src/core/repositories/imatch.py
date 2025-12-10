"""A repository interface for match entity."""

from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.match import Match, MatchBroker, MatchUpdateIn


class IMatchRepository(ABC):
    """An abstract repository class for match."""

    @abstractmethod
    async def get_match_by_id(self, match_id: int) -> Match | None:
        """Get match by ID.

        Args:
            match_id (int): The ID of the match.

        Returns:
            Match | None: The match object if exists.
        """

    @abstractmethod
    async def get_all_matches(self) -> Iterable[Match]:
        """Get all matches.

        Returns:
            Iterable[Match]: The collection of all matches.
        """

    @abstractmethod
    async def get_matches_by_league(self, league_id: int) -> Iterable[Match]:
        """Get all matches in a league.

        Args:
            league_id (int): The ID of the league.

        Returns:
            Iterable[Match]: The collection of matches in the league.
        """

    @abstractmethod
    async def get_matches_by_team(self, team_id: int) -> Iterable[Match]:
        """Get all matches for a team (home or away).

        Args:
            team_id (int): The ID of the team.

        Returns:
            Iterable[Match]: The collection of matches for the team.
        """

    @abstractmethod
    async def create_match(self, data: MatchBroker) -> Match | None:
        """Create a new match.

        Args:
            data (MatchBroker): The match input data.

        Returns:
            Match | None: The created match object.
        """

    @abstractmethod
    async def update_match(
        self, 
        match_id: int, 
        data: MatchUpdateIn
    ) -> Match | None:
        """Update match score and/or date.

        Args:
            match_id (int): The ID of the match.
            data (MatchUpdateIn): The updated match data.

        Returns:
            Match | None: The updated match object.
        """

    @abstractmethod
    async def delete_match(self, match_id: int) -> bool:
        """Delete a match.

        Args:
            match_id (int): The id of the match.

        Returns:
            bool: Success of the operation.
        """