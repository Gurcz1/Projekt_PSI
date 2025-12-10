"""A module containing league endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.league import LeagueIn, LeagueUpdate, LeagueBroker, League
from src.infrastructure.dto.leaguedto import LeagueDTO
from src.infrastructure.services.ileague import ILeagueService
from src.infrastructure.services.iteam import ITeamService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=LeagueDTO, status_code=201)
@inject
async def create_league(
    league: LeagueIn,
    service: ILeagueService = Depends(Provide[Container.league_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for creating a new league.

    Args:
        league (LeagueIn): The league data.
        service (ILeagueService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new league attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))

    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    league_broker = LeagueBroker(**league.model_dump(), owner_id=int(user_id))
    new_league = await service.add_league(league_broker)

    return new_league.model_dump() if new_league else {}


@router.get("/all", response_model=Iterable[LeagueDTO], status_code=200)
@inject
async def get_all_leagues(
    service: ILeagueService = Depends(Provide[Container.league_service]),
) -> Iterable:
    """An endpoint for getting all public leagues.

    Args:
        service (ILeagueService, optional): The injected service dependency.

    Returns:
        Iterable: The league attributes collection.
    """
    leagues = await service.get_public_leagues()
    return leagues


@router.get("/by-city", response_model=Iterable[LeagueDTO], status_code=200)
@inject
async def get_leagues_by_city(
    city: str,
    service: ILeagueService = Depends(Provide[Container.league_service]),
) -> Iterable:
    """An endpoint for getting all public leagues filtered by city.

    Args:
        city (str): The city name to filter by.
        service (ILeagueService, optional): The injected service dependency.

    Returns:
        Iterable: The league attributes collection.
    """
    leagues = await service.get_leagues_by_city(city)
    return leagues


@router.get("/my", response_model=Iterable[LeagueDTO], status_code=200)
@inject
async def get_my_leagues(
    service: ILeagueService = Depends(Provide[Container.league_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting all leagues owned by the current user.

    Args:
        service (ILeagueService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: The league attributes collection.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))

    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    leagues = await service.get_my_leagues(user_id)

    return leagues


@router.get("/archived", response_model=Iterable[LeagueDTO], status_code=200)
@inject
async def get_archived_leagues(
    service: ILeagueService = Depends(Provide[Container.league_service]),
) -> Iterable:
    """An endpoint for getting all archived leagues.

    Args:
        service (ILeagueService, optional): The injected service dependency.

    Returns:
        Iterable: The archived league attributes collection.
    """

    leagues = await service.get_archived_leagues()

    return leagues


@router.get(
        "/{league_id}", 
        response_model=LeagueDTO, 
        status_code=200
)
@inject
async def get_league_by_id(
    league_id: int,
    service: ILeagueService = Depends(Provide[Container.league_service]),
) -> dict | None:
    """An endpoint for getting league by ID.

    Args:
        league_id (int): The ID of the league.
        service (ILeagueService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if league does not exist.

    Returns:
        dict | None: The league details.
    """

    if league := await service.get_by_id(league_id):
        return league.model_dump()

    raise HTTPException(status_code=404, detail="League not found")


@router.post(
        "/{league_id}/archive", 
        response_model=LeagueDTO, 
        status_code=201
)
@inject
async def archive_league(
    league_id: int,
    service: ILeagueService = Depends(Provide[Container.league_service]),
) -> dict:
    """An endpoint for archiving a league.

    Args:
        league_id (int): The ID of the league.
        service (ILeagueService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if league does not exist.

    Returns:
        dict: The updated league details.
    """

    if updated_league := await service.archive_league(league_id):
        return updated_league.model_dump()

    raise HTTPException(status_code=404, detail="League not found")


@router.put("/{league_id}", response_model=LeagueDTO, status_code=201)
@inject
async def update_league(
    league_id: int,
    league_update: LeagueUpdate,
    service: ILeagueService = Depends(Provide[Container.league_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating a league.

    Args:
        league_id (int): The ID of the league.
        league_update (LeagueUpdate): The updated league details.
        service (ILeagueService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if league does not exist.
        HTTPException: 403 if user is not the league owner.

    Returns:
        dict: The updated league details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))

    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if updated_league := await service.update_league(league_id, league_update, user_id):
        return updated_league.model_dump()

    raise HTTPException(status_code=404, detail="League not found")


@router.delete("/{league_id}", status_code=204)
@inject
async def delete_league(
    league_id: int,
    service: ILeagueService = Depends(Provide[Container.league_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting a league.

    Args:
        league_id (int): The ID of the league.
        service (ILeagueService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if league does not exist.
        HTTPException: 403 if user is not the league owner.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))

    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if await service.get_by_id(league_id):
        await service.delete_league(league_id, user_id)
        return

    raise HTTPException(status_code=404, detail="League not found")

@router.get("/{league_id}/standings", response_model=Iterable[League], status_code=200)
@inject
async def get_standings(
    league_id: int,
    service: ILeagueService = Depends(Provide[Container.league_service]),
) -> Iterable:
    
    standings = await service.get_standings(league_id)
    
    return standings
