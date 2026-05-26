from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ...domain.interfaces.entity_interface import IEntity
from ...models.models import EntityModel


class EntityRepository(BaseRepository[EntityModel], IEntity):
    ''' Repository class for entity-related database operations.
        - Implements the IEntity interface, providing concrete implementations for creating, retrieving, updating, soft-deleting, and restoring entities.
        - Inherits from BaseRepository to leverage common CRUD operations and reduce code duplication.
        - Interacts with the database using SQLAlchemy's AsyncSession to perform asynchronous operations on the EntityModel.
    '''
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, EntityModel)