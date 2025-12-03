"""A repository for team entity."""


from abc import ABC, abstractmethod
from typing import Iterable, Any

from src.core.domain.team import Team, TeamBroker, TeamIn

class ITeamRepository(ABC):


    @abstractmethod
    async def get_team_by_id(self, team_id: int) -> Team | None:
        """"""

    
    @abstractmethod
    async def get_all_teams(self) -> Iterable[Team]:
        """"""

    @abstractmethod
    async def get_teams_by_league(
        self,
        team_id: int,
    ) -> Iterable[Team]:
         """"""
    
    @abstractmethod
    async def create_team(self, data: TeamBroker) -> Any | None:
        """"""
    

    @abstractmethod
    async def update_team(
        self,
        team_id: int,
        data: TeamIn,
    ) -> Team | None:
        """"""


    @abstractmethod
    async def delete_team(self, team_id: int) -> bool:
            """"""