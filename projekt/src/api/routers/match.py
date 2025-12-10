"""A module containing match endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.core.domain.match import Match, MatchBroker, MatchIn, MatchUpdateIn
from src.infrastructure.services.imatch import IMatchService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Match, status_code=201)
@inject
async def create_match(
    match: MatchIn,
    service: IMatchService = Depends(Provide[Container.match_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Create a new match in a league.
    
    Args:
        match: Match data (league_id, home_team_id, away_team_id, date)
        service: Injected match service
        credentials: JWT token for authentication
        
    Returns:
        Created match data
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
    
    match_broker = MatchBroker(
        submitted_by=user_id,
        **match.model_dump(),
    )
    new_match = await service.create_match(match_broker)

    if not new_match:
        raise HTTPException(
            status_code=400,
            detail="Could not create match. League may not exist, may be inactive, or teams may not belong to the league."
        )

    return new_match.model_dump()


@router.get("/all", response_model=Iterable[Match], status_code=200)
@inject
async def get_all_matches(
    service: IMatchService = Depends(Provide[Container.match_service]),
) -> Iterable:
    """Get all matches.

    Returns:
        All matches collection.
    """
    return await service.get_all_matches()


@router.get("/league/{league_id}", response_model=Iterable[Match], status_code=200)
@inject
async def get_matches_by_league(
    league_id: int,
    service: IMatchService = Depends(Provide[Container.match_service]),
) -> Iterable:
    """Get all matches in a league.

    Args:
        league_id: The ID of the league.

    Returns:
        Matches in the league.
    """
    return await service.get_matches_by_league(league_id)


@router.get("/team/{team_id}", response_model=Iterable[Match], status_code=200)
@inject
async def get_matches_by_team(
    team_id: int,
    service: IMatchService = Depends(Provide[Container.match_service]),
) -> Iterable:
    """Get all matches for a team.

    Args:
        team_id: The ID of the team.

    Returns:
        Matches for the team.
    """
    return await service.get_matches_by_team(team_id)


@router.get("/{match_id}", response_model=Match, status_code=200)
@inject
async def get_match_by_id(
    match_id: int,
    service: IMatchService = Depends(Provide[Container.match_service]),
) -> dict:
    """Get match by ID.

    Args:
        match_id: The ID of the match.

    Returns:
        Match details.
    """
    match = await service.get_match_by_id(match_id)
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return match.model_dump()


@router.put("/{match_id}", response_model=Match, status_code=200)
@inject
async def update_match(
    match_id: int,
    match_update: MatchUpdateIn,
    service: IMatchService = Depends(Provide[Container.match_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Update match score and/or date.

    Args:
        match_id: The ID of the match.
        match_update: The updated match data.

    Returns:
        Updated match details.
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

    updated_match = await service.update_match(match_id, match_update)
    
    if not updated_match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return updated_match.model_dump()


@router.delete("/{match_id}", status_code=204)
@inject
async def delete_match(
    match_id: int,
    service: IMatchService = Depends(Provide[Container.match_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """Delete a match.

    Args:
        match_id: The ID of the match.
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

    if not await service.delete_match(match_id):
        raise HTTPException(status_code=404, detail="Match not found")
