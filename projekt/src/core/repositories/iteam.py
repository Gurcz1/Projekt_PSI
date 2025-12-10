"""A repository for team entity."""


from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.team import Team, TeamBroker, TeamIn

class ITeamRepository(ABC):
    """An abstract repository class for team."""

    @abstractmethod
    async def get_team_by_id(self, team_id: int) -> Team | None:
        """Get team by ID.

        Args:
            team_id (int): The ID of the team.

        Returns:
            Team | None: The team object if exists.
        """

    @abstractmethod
    async def get_all_teams(self) -> Iterable[Team]:
        """Get all teams.

        Returns:
            Iterable[Team]: The collection of all teams.
        """

    @abstractmethod
    async def get_teams_by_league(
        self,
        league_id: int,
    ) -> Iterable[Team]:
        """Get all teams in a league.

        Args:
            league_id (int): The ID of the league.

        Returns:
            Iterable[Team]: The collection of teams in the league.
        """
    
    @abstractmethod
    async def create_team(self, data: TeamBroker) -> Any | None:
        """Create a new team.

        Args:
            data (TeamBroker): The team input data with captain ID.

        Returns:
            Any | None: The created team object.
        """
    
    @abstractmethod
    async def update_team(
        self,
        team_id: int,
        data: TeamIn,
    ) -> Team | None:
        """Update team data.

        Args:
            team_id (int): The ID of the team.
            data (TeamIn): The updated team details.

        Returns:
            Team | None: The updated team object.
        """

    @abstractmethod
    async def delete_team(self, team_id: int) -> bool:
        """Delete a team.

        Args:
            team_id (int): The ID of the team.

        Returns:
            bool: Success of the operation.
        """