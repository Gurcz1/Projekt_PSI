"""A service for league entity."""

from typing import Any, Iterable
from fastapi import HTTPException, status

from src.infrastructure.dto.leaguedto import LeagueDTO
from src.core.domain.league import League, LeagueBroker
from src.core.repositories.ileague import ILeagueRepository
from src.core.repositories.imatch import IMatchRepository
from src.core.repositories.iteam import ITeamRepository
from src.infrastructure.services.ileague import ILeagueService


class LeagueService(ILeagueService):
    """An implementation of service class for league."""

    def __init__(
        self, 
        repository: ILeagueRepository, 
        match_repository: IMatchRepository, 
        team_repository: ITeamRepository
    ) -> None:
        """The initializer of the `league service`.

        Args:
            repository (ILeagueRepository): The reference to the repository.
        """
        self._repository = repository
        self._match_repository = match_repository
        self._team_repository = team_repository

    async def add_league(self, data: LeagueBroker) -> LeagueDTO | None:
        """A method creating a new league.

        Args:
            data (LeagueBroker): The league input data with owner_id.

        Returns:
            LeagueDTO | None: The new league object.
        """
        return await self._repository.add_league(data)

    async def get_public_leagues(self) -> Iterable[LeagueDTO]:
        """A method getting all public leagues.

        Returns:
            Iterable[LeagueDTO]: A list of public leagues.
        """
        return await self._repository.get_all_public()

    async def get_leagues_by_city(self, city: str) -> Iterable[LeagueDTO]:
        """A method getting all leagues by city name.

        Args:
            city (str): The city name to search for.

        Returns:
            Iterable[LeagueDTO]: A list of leagues in the specified city.
        """
        return await self._repository.get_by_city(city)

    async def get_my_leagues(self, user_id: int) -> Iterable[LeagueDTO]:
        """A method getting all leagues owned by the user.
    
        Args:
            user_id (int): The ID of the user.

        Returns:
            Iterable[LeagueDTO]: A list of leagues owned by the user.
        """
        return await self._repository.get_by_owner(user_id)

    async def get_by_id(self, league_id: int) -> Any | None:
        """A method getting league by ID.

        Args:
            league_id (int): The ID of the league.

        Returns:
            Any | None: The league object.
        """
        return await self._repository.get_by_id(league_id)
    
    async def archive_league(self, league_id: int) -> LeagueDTO | None:
        """A method archiving a league.

        Args:
            league_id (int): The ID of the league.

        Returns:
            LeagueDTO | None: The updated league object.
        """
        return await self._repository.archive_league(league_id)

    async def delete_league(self, league_id: int, user_id: int) -> bool:
        """A method deleting a league.

        Args:
            league_id (int): The ID of the league.
            user_id (int): The ID of the user requesting deletion.

        Returns:
            bool: True if deleted successfully.
            
        Raises:
            HTTPException: If user is not the league owner.
        """
        league = await self._repository.get_by_id(league_id)
        if not league:
            raise HTTPException(status_code=404, detail="League not found")
        
        if league.owner.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the league owner can delete the league"
            )
        
        return await self._repository.delete_league(league_id)

    async def update_league(
            self, 
            league_id: int, 
            league_update: LeagueBroker, 
            user_id: int,
        ) -> LeagueDTO | None:
        """Updates a league.

        Args:
            league_id: League ID
            league_update: Update data
            user_id: User requesting update

        Returns:
            Updated league object.

        Raises:
            HTTPException: If user is not the league owner.
        """
        league = await self._repository.get_by_id(league_id)
        if not league:
            raise HTTPException(status_code=404, detail="League not found")

        if league.owner.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the league owner can update the league"
            )

        return await self._repository.update_league(league_id, league_update)

    async def get_archived_leagues(self) -> Iterable[LeagueDTO]:
        """Get all archived leagues.

        Returns:
            Iterable[LeagueDTO]: A list of archived leagues.
        """
        return await self._repository.get_all_archived()

    async def get_standings(self, league_id: int) -> Iterable[Any]:

        teams = await self.team_repository.get_league_by_id(league_id)

        all_matches = await self.match_repository.get_league_by_id(league_id)

        matches = [match for match in all_matches if match.status == 'finished']

        standings = {}
        for team in teams:
            standings[str(team.id)] = {
                "team_id": str(team.id),
                "team_name": team.name,
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_difference": 0,
                "points": 0,
            }

        for match in matches:
            home_id = str(match.home_team_id)
            away_id = str(match.away_team_id)
            
            if home_id not in standings or away_id not in standings:
                continue

            home_score = match.home_score or 0
            away_score = match.away_score or 0

            standings[home_id]["played"] += 1
            standings[away_id]["played"] += 1
            
            standings[home_id]["goals_for"] += home_score
            standings[home_id]["goals_against"] += away_score
            standings[away_id]["goals_for"] += away_score
            standings[away_id]["goals_against"] += home_score
            
            if home_score > away_score:
                standings[home_id]["won"] += 1
                standings[home_id]["points"] += 3
                standings[away_id]["lost"] += 1
            elif home_score < away_score:
                standings[away_id]["won"] += 1
                standings[away_id]["points"] += 3
                standings[home_id]["lost"] += 1
            else:
                standings[home_id]["drawn"] += 1
                standings[away_id]["drawn"] += 1
                standings[home_id]["points"] += 1
                standings[away_id]["points"] += 1
                
        for team_id in standings:
            standings[team_id]["goal_difference"] = (
                standings[team_id]["goals_for"] - standings[team_id]["goals_against"]
            )
            
        sorted_standings = sorted(
            standings.values(),
            key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]),
            reverse=True,
        )
        
        return sorted_standings
