"""A database implementation of league repository."""

from typing import Any, List
from sqlalchemy import select, join

from src.core.domain.league import LeagueBroker, LeagueStatus, League
from src.core.repositories.ileague import ILeagueRepository
from src.db import (
    database, 
    league_table, 
    user_table,
)
from src.infrastructure.dto.leaguedto import LeagueDTO


class LeagueRepository(ILeagueRepository):
    """An implementation of repository class for league."""

    async def add_league(self, league: LeagueBroker) -> LeagueDTO | None:
        """The method adding new league to the data storage.

        Args:
            league (LeagueBroker): A league object with owner_id included.

        Returns:
            LeagueDTO | None: The new league object with owner information.
        """
        league_data = league.model_dump()
        league_data['status'] = LeagueStatus.ACTIVE.value
        query = league_table.insert().values(**league_data)
        new_league_id = await database.execute(query)
        
        return await self.get_by_id(new_league_id)

    async def get_all_public(self) -> List[LeagueDTO]:
        """The method getting all public leagues.

        Returns:
            List[LeagueDTO]: A list of public leagues with owner information.
        """
        query = (
            select(league_table, user_table)
            .select_from(
                join(league_table, user_table, 
                     league_table.c.owner_id == user_table.c.id)
            )
            .where(league_table.c.status == LeagueStatus.ACTIVE)
            .order_by(league_table.c.id.asc())
        )
        leagues = await database.fetch_all(query)

        return [LeagueDTO.from_record(league) for league in leagues]

    async def get_by_owner(self, owner_id: int) -> List[LeagueDTO]:
        """The method getting all leagues owned by a user.

        Args:
            owner_id (int): The ID of the owner.

        Returns:
            List[LeagueDTO]: A list of leagues owned by the user with owner information.
        """
        query = (
            select(league_table, user_table)
            .select_from(
                join(league_table, user_table, 
                     league_table.c.owner_id == user_table.c.id)
            )
            .where(league_table.c.owner_id == owner_id)
            .order_by(league_table.c.name.asc())
        )
        leagues = await database.fetch_all(query)

        return [LeagueDTO.from_record(league) for league in leagues]

    async def get_all_archived(self) -> List[LeagueDTO]:
        """The method getting all archived leagues.

        Returns:
            List[LeagueDTO]: A list of archived leagues with owner information.
        """
        query = (
            select(league_table, user_table)
            .select_from(
                join(league_table, user_table, 
                     league_table.c.owner_id == user_table.c.id)
            )
            .where(league_table.c.status == LeagueStatus.ARCHIVED)
        )
        leagues = await database.fetch_all(query)
        return [LeagueDTO.from_record(league) for league in leagues]

    async def get_by_id(self, league_id: int) -> Any | None:
        """The method getting league by ID.

        Args:
            league_id (int): The ID of the league.

        Returns:
            Any | None: The league object with owner information.
        """
        query = (
            select(league_table, user_table)
            .select_from(
                join(
                    league_table, 
                    user_table, 
                    league_table.c.owner_id == user_table.c.id)
            )
            .where(league_table.c.id == league_id)
            .order_by(league_table.c.name.asc())
        )
        league = await database.fetch_one(query)

        return LeagueDTO.from_record(league) if league else None

    async def archive_league(self, league_id: int) -> LeagueDTO | None:
        """The method archiving a league.

        Args:
            league_id (int): The ID of the league.

        Returns:
            LeagueDTO | None: The updated league object with owner information.
        """
        query = league_table \
            .update() \
            .where(league_table.c.id == league_id) \
            .values(status=LeagueStatus.ARCHIVED)
        await database.execute(query)

        return await self.get_by_id(league_id)

    async def delete_league(self, league_id: int) -> bool:
        """The method deleting a league.

        Args:
            league_id (int): The ID of the league.

        Returns:
            bool: True if deleted successfully.
        """
        if await self.get_by_id(league_id):
            query = league_table \
                .delete() \
                .where(league_table.c.id == league_id)
            await database.execute(query)

            return True

        return False

    async def update_league(
        self,
        league_id: int,
        data: LeagueBroker,
    ) -> Any | None:
        """The method updating league data in the data storage.

        Args:
            league_id (int): The ID of the league.
            data (LeagueBroker): The updated league details.

        Returns:
            League | None: The updated league details.
        """

        if await self.get_by_id(league_id):
            query = (
                league_table.update()
                .where(league_table.c.id == league_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            league = await self.get_by_id(league_id)

            return league

        return None

    async def get_by_city(self, city: str) -> List[LeagueDTO]:
        """Get leagues by city name.

        Args:
            city (str): The city name.

        Returns:
            List[LeagueDTO]: List of leagues in the city.
        """
        query = (
            select(league_table, user_table)
            .select_from(
                join(
                    league_table, 
                    user_table, 
                    league_table.c.owner_id == user_table.c.id)
            )
            .where(
                (league_table.c.city.ilike(f"%{city}%")) &
                (league_table.c.status == LeagueStatus.ACTIVE)
            )
            .order_by(league_table.c.name.asc())
        )
        leagues = await database.fetch_all(query)

        return [LeagueDTO.from_record(league) for league in leagues]
