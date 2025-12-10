"""A repository for match entity."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join, or_

from src.core.domain.match import MatchBroker, Match, MatchIn, MatchUpdateIn
from src.core.repositories.imatch import IMatchRepository
from src.db import (
    database, 
    team_table, 
    league_table,
    match_table,
)
from src.core.domain.league import LeagueStatus

class MatchRepository(IMatchRepository):

    async def create_match(self, data: MatchBroker) -> Any | None:
        """Create a new match."""

        league_query = (
            league_table.select()
            .where(
                (league_table.c.id == data.league_id) &
                (league_table.c.status == LeagueStatus.ACTIVE)
            )
        )
        league = await database.fetch_one(league_query)

        if not league:
            return None

        if league['owner_id'] != data.submitted_by:
            return None

        team_home_query = (
            team_table.select()
            .where(
                (team_table.c.id == data.home_team_id) &
                (team_table.c.league_id == data.league_id)
            )
        )
        team_home = await database.fetch_one(team_home_query)

        if not team_home:
            return None

        team_away_query = (
            team_table.select()
            .where(
                (team_table.c.id == data.away_team_id) &
                (team_table.c.league_id == data.league_id)
            )
        )
        team_away = await database.fetch_one(team_away_query)

        if not team_away:
            return None

        insert_data = data.model_dump()
        insert_data['status'] = 'scheduled'
        
        query = match_table.insert().values(**insert_data)
        new_match_id = await database.execute(query)
        new_match = await self._get_match_by_id(new_match_id)

        return Match(**dict(new_match)) if new_match else None

    async def get_match_by_id(self, match_id: int) -> Any | None:
        """The method getting match by ID."""

        match = await self._get_match_by_id(match_id)

        return Match(**dict(match)) if match else None
        
    async def get_all_matches(self) -> Iterable[Any]:
        """The method getting all matches."""

        query = match_table.select().order_by(match_table.c.date.asc())
        matches = await database.fetch_all(query)

        return [Match(**dict(match)) for match in matches]

    async def get_matches_by_league(self, league_id: int) -> Iterable[Any]:
        """The method getting all matches by league ID."""

        query = match_table \
            .select() \
            .where(match_table.c.league_id == league_id) \
            .order_by(match_table.c.date.asc())
        matches = await database.fetch_all(query)

        return [Match(**dict(match)) for match in matches]

    async def get_matches_by_team(self, team_id: int) -> Iterable[Any]:
        """The method getting all matches by team ID (home or away)."""

        query = match_table \
            .select() \
            .where(
                or_(
                    match_table.c.home_team_id == team_id,
                    match_table.c.away_team_id == team_id
                )
            ) \
            .order_by(match_table.c.date.asc())
        matches = await database.fetch_all(query)

        return [Match(**dict(match)) for match in matches]

    async def update_match(
        self, 
        match_id: int, 
        data: MatchUpdateIn
    ) -> Match | None:
        """Update match score and/or date."""

        if not await self._get_match_by_id(match_id):
            return None
        
        update_data = data.model_dump(exclude_none=True)
        
        if not update_data:
            return await self.get_match_by_id(match_id)

        # Jeśli podano wynik, ustaw status na finished
        if 'home_score' in update_data and 'away_score' in update_data:
            update_data['status'] = 'finished'

        query = (
            match_table.update()
            .where(match_table.c.id == match_id)
            .values(**update_data)
        )
        await database.execute(query)

        updated_match = await self._get_match_by_id(match_id)
        return Match(**dict(updated_match)) if updated_match else None

    async def delete_match(self, match_id: int) -> bool:
        """The method deleting a match from the data storage."""

        if await self._get_match_by_id(match_id):
            query = match_table \
                .delete() \
                .where(match_table.c.id == match_id)
            await database.execute(query)

            return True

        return False

    async def _get_match_by_id(self, match_id: int) -> Record | None:
        """A private method getting match from the DB based on its ID."""

        query = (
            match_table.select()
            .where(match_table.c.id == match_id)
        )

        return await database.fetch_one(query)

