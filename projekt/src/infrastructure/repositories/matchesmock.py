from typing import Iterable

from src.core.domain.match import Match, MatchIn
from src.core.repositories.imatch import IMatchRepository
from src.infrastructure.repositories.db import mathches

class MatchMockRepository(IMatchRepository):
    
    async def get_all_matches(self) -> Iterable[Match]:
        
        return mathches
    
    async def get_by_league(self, league_id: int) -> Iterable[Match]:
        
        return filter(lambda x: x.league_id == league_id, mathches)
    
    async def get_by_team(self, team_id: int) -> Iterable[Match]:
        
        return mathches
    
    async def get_by_id(self, match_id: int) -> Match | None:

        return next((obj for obj in mathches if obj.id == match_id), None)
    
    async def add_match(self, data: MatchIn) -> None:

        mathches.append(data)

    async def update_airport(
        self,
        match_id: int,
        data: MatchIn,
    ) -> Match | None:
        
        if match_pos := \
                next(filter(lambda x: x.id == match_id, mathches)):
            mathches[match_pos] = data

            return Match(id=0, **data.model_dump())

        return None

    async def delete_match(self, match_id: int) -> bool:


        if match_pos := \
                next(filter(lambda x: x.id == match_id, mathches)):
            mathches.remove(match_pos)
            return True

        return False