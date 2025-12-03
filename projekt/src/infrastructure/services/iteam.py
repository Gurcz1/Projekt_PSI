"""Module containing team service abstractions."""

from abc import ABC, abstractmethod

from typing import Iterable

from src.core.domain.team import Team, TeamBroker, TeamIn


class ITeamService(ABC):
    """An abstract class representing protocol of team repository."""

    @abstractmethod
    async def get_team_by_id(self, team_id: int) -> Team | None:
        """The abstract getting a team from the repository.

        Args:
            team_id (int): The id of the team.

        Returns:
            Team | None: The team data if exists.
        """

    @abstractmethod
    async def get_all_teams(self) -> Iterable[Team]:
        """The abstract getting all teams from the repository.

        Returns:
            Iterable[Team]: The collection of the all teams.
        """

    @abstractmethod
    async def get_teams_by_league(
        self,
        team_id: int,
    ) -> Iterable[Team]:
        """The abstract getting all provided leagues's teams
            from the repository.

        Args:
            team_id (int): The id of the team.

        Returns:
            Iterable[Team]: The collection of the teams.
        """

    @abstractmethod
    async def create_team(self, data: TeamBroker) -> None:
        """The abstract adding new team to the repository.

        Args:
            data (TeamBroker): The attributes of the team. 
        """

    @abstractmethod
    async def update_team(
        self,
        team_id: int,
        data: TeamIn,
    ) -> Team | None:
        """The abstract updating team data in the repository.

        Args:
            team_id (int): The team id.
            data (TeamIn): The attributes of the team.

        Returns:
            Team | None: The updated team.
        """

    @abstractmethod
    async def delete_team(self, team_id: int) -> bool:
        """The abstract updating removing team from the repository.

        Args:
            team_id (int): The team id.

        Returns:
            bool: Success of the operation.
        """