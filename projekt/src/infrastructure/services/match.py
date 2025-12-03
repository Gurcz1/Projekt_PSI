from typing import Iterable

from projekt.src.core.domain.match import Match, MatchIn
from projekt.src.core.repositories.imatch import IMatchRepository
from projekt.src.infrastructure.services.imatch import IMatchService

class MatchService(IMatchService):
    
    _repository = IMatchRepository
    
    
    def __init__(self, repository: IMatchRepository) -> None:
        
        self._repository = repository
        