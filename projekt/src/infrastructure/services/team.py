

from typing import Iterable

from src.core.domain.team import Team, TeamBroker
from src.core.repositories.iteam import ITeamRepository
from src.infrastructure.services.iteam import ITeamService


class TeamService(ITeamService):
    """A class implementing team service"""

    _repository: ITeamRepository

    def __init__(self, repository: ITeamRepository) -> None:
        """The initializer of the `team service`.

        Args:
            repository (ITeamRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_team_by_id(self, team_id: int) -> Team | None:

        return await self._repository.get_team_by_id(team_id)

    async def get_all_teams(self) -> Iterable[Team]:

        return await self._repository.get_all_teams()

    async def get_teams_by_league(
        self,
        league_id: int,
    ) -> Iterable[Team]:

        return await self._repository.get_teams_by_league(league_id)

    async def create_team(self, data: TeamBroker) ->  Team | None:

        return await self._repository.create_team(data)

    async def update_team(
        self,
        team_id: int,
        data: TeamBroker
    ) -> Team | None:

        return await self._repository.update_team(
            team_id=team_id,
            data=data,
        )
    
    async def delete_team(self, team_id:int) -> bool:


        return await self._repository.delete_team(team_id)