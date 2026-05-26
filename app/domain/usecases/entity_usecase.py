from .base_usecase import BaseUseCase
from ..interfaces.entity_interface import IEntity


class EntityUseCase(BaseUseCase):
    ''' Use case class for entity-related operations.
        - Encapsulates the business logic for creating, retrieving, updating, soft-deleting, and restoring entities.
        - Interacts with the entity repository to perform database operations.
    '''
    def __init__(self, repo: IEntity, response_schema=None):
        super().__init__(repo, response_schema)