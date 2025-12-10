from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.core.domain.team import Team, TeamBroker, TeamIn
from src.infrastructure.services.iteam import ITeamService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Team, status_code=201)
@inject
async def create_team(
    team: TeamIn,
    service: ITeamService = Depends(Provide[Container.team_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Create a new team in a league."""
    
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))
    
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    extended_team_data = TeamBroker(
        captain_id=user_id,
        **team.model_dump(),
    )
    new_team = await service.create_team(extended_team_data)

    if not new_team:
        raise HTTPException(
            status_code=400,
            detail="Could not create team. League may not exist, may be inactive, may be private, or you may already have a team in this league."
        )

    return new_team.model_dump()

<<<<<<< HEAD
=======

>>>>>>> 1b531bd07331be965cc9d6b99d045f24c7cab3b2
@router.get("/all", response_model=Iterable[Team], status_code=200)
@inject
async def get_all_teams(
    service: ITeamService = Depends(Provide[Container.team_service]),
) -> Iterable:
<<<<<<< HEAD
    
    teams = await service.get_all_teams()
    
    return teams
=======
    """Get all teams."""
    return await service.get_all_teams()


@router.get("/league/{league_id}", response_model=Iterable[Team], status_code=200)
@inject
async def get_teams_by_league(
    league_id: int,
    service: ITeamService = Depends(Provide[Container.team_service]),
) -> Iterable:
    """Get all teams in a league."""
    return await service.get_teams_by_league(league_id)

>>>>>>> 1b531bd07331be965cc9d6b99d045f24c7cab3b2

@router.get("/{team_id}", response_model=Team, status_code=200)
@inject
async def get_team_by_id(
    team_id: int,
    service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
<<<<<<< HEAD
    
    if team := await service.get_team_by_id(team_id=team_id):
        return team.model_dump()

    raise HTTPException(status_code=404, detail="Team not found")

@router.get(
    "/league/{league_id}",
    response_model=list[Team],
    status_code=200,
)
@inject
async def get_team_by_league(
    league_id: int,
    service: ITeamService = Depends(Provide[Container.team_service]),
) -> Iterable:
    
    teams = await service.get_teams_by_league(league_id)
    
    return teams

@router.put("/{team_id}", response_model=Team, status_code=201)
@inject
async def update_team(
    team_id: int,
    updated_team: TeamIn,
    service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    
    if await service.get_team_by_id(team_id=team_id):
        new_updated_team = await service.update_team(
            team_id=team_id,
            data=updated_team,
        )
        return new_updated_team.model_dump() if new_updated_team else {}
    
    raise HTTPException(status_code=404, detail="Team not found")
=======
    """Get team by ID."""
    team = await service.get_team_by_id(team_id)
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return team.model_dump()


@router.put("/{team_id}", response_model=Team, status_code=200)
@inject
async def update_team(
    team_id: int,
    team_update: TeamIn,
    service: ITeamService = Depends(Provide[Container.team_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Update team data."""
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))
    
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    updated_team = await service.update_team(team_id, team_update)
    
    if not updated_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return updated_team.model_dump()

>>>>>>> 1b531bd07331be965cc9d6b99d045f24c7cab3b2

@router.delete("/{team_id}", status_code=204)
@inject
async def delete_team(
    team_id: int,
    service: ITeamService = Depends(Provide[Container.team_service]),
<<<<<<< HEAD
) -> None:
    
    if await service.get_team_by_id(team_id=team_id):
        await service.delete_team(team_id)
        
        return
    
    raise HTTPException(status_code=404, detail="Team not found")
=======
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """Delete a team."""
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_id = int(token_payload.get("sub"))
    
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if not await service.delete_team(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
>>>>>>> 1b531bd07331be965cc9d6b99d045f24c7cab3b2
