from typing import Iterable

from src.core.domain.team import Team, TeamIn
from src.core.repositories.iteam import ITeamRepository
from src.infrastructure.repositories.db import teams

class TeamMockRepository(ITeamRepository):
    
    
    async def get_team_by_id(self, team_id: int) -> Team | None:

        return next(
            (obj for obj in teams if obj.id == team_id),
            None,
        )
    
    async def get_teams_by_league(
        self, 
        league_id: int,
    ) -> Iterable[Team]:

        return filter(lambda x: x.league_id == league_id, teams)
    
    async def add_team(self, data: TeamIn) -> Team | None:

        teams.append(data)

    async def update_team(
            self,
            team_id: int,
            data: TeamIn,
    ) -> Team | None:
        if team_pos := \
                next(filter(lambda x: x.id == team_id, teams)):
            teams[team_pos] = data

            return Team(id=0, **data.model_dump())

        return None
    
    async def delete_team(self, team_id: int) -> bool:

        if team_pos := \
                next(filter(lambda x: x.id == team_id, teams)):
            teams.remove(team_pos)
            return True

        return False
    
    async def get_all_teams(self) -> Iterable[Team]:
        
        return teams