"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.leaguedb import LeagueRepository
from src.infrastructure.repositories.teamdb import TeamRepository
from src.infrastructure.repositories.matchdb import MatchRepository
from src.infrastructure.services.user import UserService
from src.infrastructure.services.league import LeagueService
from src.infrastructure.services.team import TeamService
from src.infrastructure.services.match import MatchService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    user_repository = Singleton(UserRepository)
    league_repository = Singleton(LeagueRepository)
    team_repository = Singleton(TeamRepository)
    match_repository = Singleton(MatchRepository)

    user_service = Factory(
        UserService,
        repository=user_repository,
    )
    league_service = Factory(
        LeagueService,
        repository=league_repository,
    )
    team_service = Factory(
        TeamService,
        repository=team_repository,
    )
    match_service = Factory(
        MatchService,
        repository=match_repository,
    )
