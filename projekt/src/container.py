"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.leaguedb import LeagueRepository
from src.infrastructure.services.user import UserService
from src.infrastructure.services.league import LeagueService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    user_repository = Singleton(UserRepository)
    league_repository = Singleton(LeagueRepository)


    user_service = Factory(
        UserService,
        repository=user_repository,
    )
    league_service = Factory(
        LeagueService,
        repository=league_repository,
    )
    
