from typing import Iterable

from src.core.domain.league import League, LeagueIn
from src.core.repositories.ileague import ILeagueRepository
from src.infrastructure.repositories.db import leagues

class LeagueRepository(ILeagueRepository):


    async def get_league_by_id(self, league_id: int) -> League | None:

        return next(
            (obj for obj in leagues if obj.id == league_id),
            None,
        )
    
    async def get_all_leagues(self) -> Iterable[League]:
        return leagues
    
    async def add_league(self, data: LeagueIn) -> None:

        leagues.append(data)

    async def update_league(
        self,
        league_id: int,
        data: LeagueIn,
    ) -> League | None:
        
        if league_pos := \
                next(filter(lambda x: x.id == league_id, leagues)):
            leagues[league_pos] = data

            return League(id = 0, **data.model_dump())
        
        return None
    
    async def delete_league(self, league_id: int) -> bool:

        if league_pos := \
                next(filter(lambda x: x.id == league_id, leagues)):
            leagues.remove(league_pos)
            return True
        
        return False