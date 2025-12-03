"""A repository for team entity."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from src.core.domain.team import TeamBroker, Team, TeamIn
from src.core.repositories.iteam import ITeamRepository
from src.db import (
    database, 
    team_table, 
    league_table,
)
from src.core.domain.league import LeagueStatus

class TeamRepository(ITeamRepository):


    async def create_team(self, data: TeamBroker) -> Any | None:
        """The method adding new team to the data storage.

        Args:
            data (TeamBroker): The details of the new team.

        Returns:
            Team: Full details of the newly added team.

        Returns:
            Any | None: The newly added team.
        """

        league_query = (
            league_table.select()
            .where(
                (league_table.c.id == data.league_id) &
                (league_table.c.status == LeagueStatus.ACTIVE) &
                (league_table.c.is_private == False)
            )
        )
        league = await database.fetch_one(league_query)
        
        if not league:
            return None
        
        if league['owner_id'] != data.captain_id:
            existing_team_query = (
                team_table.select()
                .where(
                    (team_table.c.league_id == data.league_id) &
                    (team_table.c.captain_id == data.captain_id)
                )
            )
            existing_team = await database.fetch_one(existing_team_query)
            
            if existing_team:
                return None

        query = team_table.insert().values(**data.model_dump())
        new_team_id = await database.execute(query)
        new_team = await self._get_team_by_id(new_team_id)

        return Team(**dict(new_team)) if new_team else None

    async def get_team_by_id(self, team_id: int) -> Any | None:

        team = await self._get_team_by_id(team_id)

        return Team(**dict(team)) if team else None

    async def get_all_teams(self) -> Iterable[Any]:

        query = team_table.select().order_by(team_table.c.name.asc())
        teams = await database.fetch_all(query)

        return [Team(**dict(team)) for team in teams]

    async def get_teams_by_league(
        self,
        league_id: int,
    ) -> Iterable[Any]:
        """The abstract getting all provided continent's countries
            from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Any]: The collection of the countries.
        """

        query = team_table \
            .select() \
            .where(team_table.c.league_id == league_id) \
            .order_by(team_table.c.name.asc())
        teams = await database.fetch_all(query)

        return [Team(**dict(team)) for team in teams]

    async def update_team(
        self,
        team_id: int,
        data: TeamBroker,
    ) -> Any | None:
        """The abstract updating country data in the data storage.

        Args:
            country_id (int): The country id.
            data (CountryIn): The attributes of the country.

        Returns:
            Any | None: The updated country.
        """

        if self._get_team_by_id(team_id):
            query = (
                team_table.update()
                .where(team_table.c.id == team_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            team = await self._get_team_by_id(team_id)

            return Team(**dict(team)) if team else None

        return None

    async def delete_team(self, team_id: int) -> bool:

        if self._get_team_by_id(team_id):
            query = team_table \
                .delete() \
                .where(team_table.c.id == team_id)
            await database.execute(query)

            return True

        return False

    async def _get_team_by_id(self, team_id: int) -> Record | None:
        """A private method getting airport from the DB based on its ID.

        Args:
            airport_id (int): The ID of the airport.

        Returns:
            Any | None: Airport record if exists.
        """

        query = (
            team_table.select()
            .where(team_table.c.id == team_id)
            .order_by(team_table.c.name.asc())
        )

        return await database.fetch_one(query)