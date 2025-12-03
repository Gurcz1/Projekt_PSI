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
    """Create a new team in a league.
    
    Args:
        team: Team data (name, league_id)
        service: Injected team service
        credentials: JWT token for authentication
        
    Returns:
        Created team data
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