from typing import Generic, TypeVar, Optional, Dict, List
from fastapi import HTTPException, status

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")

class BaseUseCase(Generic[TModel, TCreate, TUpdate]):
    ''' A generic use case class providing common business logic operations for any entity type.
        - TModel: The type of the SQLAlchemy model that this use case will manage.
        - TCreate: The type of the data used for creating a new entity (e.g., a Pydantic model).
        - TUpdate: The type of the data used for updating an existing entity (e.g., a Pydantic model).
        - Provides methods for retrieving, creating, updating, and deleting entities, 
            with hooks for custom business logic before and after these operations.
    '''
    
    def __init__(self, repo, response_schema=None):
        self.repo = repo
        self.response_schema = response_schema

    # Hooks (Override in child)        
    async def before_create(self, data: Dict) -> Dict:
        ''' Hook method to execute custom logic before creating an entity.
            - data: A dictionary of the data that will be used to create the entity.
            - Can be overridden in child classes to perform actions such as validation, 
                transformation, or adding additional fields before the entity is created.
            - Returns the (potentially modified) data dictionary to be used for creation.
        '''
        return data
    
    async def before_update(self, instance: TModel, data: Dict) -> Dict:
        ''' Hook method to execute custom logic before updating an entity.
            - instance: The existing entity instance to be updated.
            - data: A dictionary of the data that will be used to update the entity.
            - Can be overridden in child classes to perform actions such as validation, 
                transformation, or adding additional fields before the entity is updated.
            - Returns the (potentially modified) data dictionary to be used for updating.
        '''
        return data
    
    async def before_delete(self, instance: TModel) -> None:
        ''' Hook method to execute custom logic before deleting an entity.
            - instance: The existing entity instance to be deleted.
            - Can be overridden in child classes to perform actions such as cleanup, 
                logging, or preventing deletion based on certain conditions before the entity is deleted.
            - Does not return anything, but can raise exceptions to prevent deletion if necessary.
        '''
        return None
    
    async def after_create(self, instance: TModel) -> TModel:
        ''' Hook method to execute custom logic after creating an entity.
            - instance: The newly created entity instance.
            - Can be overridden in child classes to perform actions such as logging, 
                sending notifications, or modifying the instance before it is returned after creation.
            - Returns the (potentially modified) entity instance to be returned after creation.
        '''
        return instance
    
    async def after_update(self, instance: TModel) -> TModel:
        ''' Hook method to execute custom logic after updating an entity.
            - instance: The updated entity instance.
            - Can be overridden in child classes to perform actions such as logging, 
                sending notifications, or modifying the instance before it is returned after update.
            - Returns the (potentially modified) entity instance to be returned after update.
        '''
        return instance
    
    # CORE METHODS
    
    async def get_by_id(self, entity_id: str) -> TModel:
        ''' Retrieves an entity by its unique identifier.
            - entity_id: The unique identifier of the entity to retrieve.
            - Uses the repository's get_by_id method to fetch the entity from the database.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Returns the retrieved entity instance.
        '''
        instance = await self.repo.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        return instance
    
    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        columns: Optional[str] = None,
        search_filter: Optional[str] = None,
        sort: Optional[str] = None,
        relations: Optional[List[str]] = None,
    ):
        ''' Retrieves a paginated list of entities with optional filtering, sorting, and related data.
            - page: The page number for pagination (default: 1).
            - limit: The number of items per page for pagination (default: 10).
            - columns: An optional string of comma-separated column names to include in the response.
            - search_filter: An optional string for filtering results based on specific criteria.
            - sort: An optional string of comma-separated column names to sort by.
            - relations: An optional list of related entities to include in the response.
            - Validates pagination parameters, applies filtering and sorting, and retrieves the results using the repository's get_all method.
            - If no results are found, returns an empty list with pagination metadata. Otherwise, returns a list of entity instances along with pagination metadata.
            - If a response schema is defined, serializes the results using the schema before returning.
            - Returns a dictionary containing the list of items and pagination metadata (total count, page number, and limit).
        '''
        # GuardRails
        if page < 1:    
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Page must be >= 1"
            )
            
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Limit must be between 1 and 100"
            )
        
        # Call repository to get results, which should return a dict with "items", "total", "page", "pages" and "page_size" aka limit
        result = await self.repo.get_all(page, limit, columns, search_filter, sort, relations)
        
        # ✅ Generic serialization
        if self.response_schema and result.get("items"):
            result["items"] = [
                self.response_schema.model_validate(item, from_attributes=True)
                for item in result["items"]
            ]

        return result
    
    async def create(self, data: TCreate) -> TModel:
        ''' Creates a new entity in the database.
            - data: The data used to create the new entity, typically a Pydantic model or a dictionary.
            - Converts the input data to a dictionary if it is a Pydantic model, then calls the before_create hook to allow for any custom logic before creation.
            - Uses the repository's create method to persist the new entity in the database, then calls the after_create hook to allow for any custom logic after creation before returning the created instance.
            - Returns the newly created entity instance.
        '''
        payload = data.model_dump() if hasattr(data, "model_dump") else data
        
        payload = await self.before_create(payload)
        
        instance = await self.repo.create(payload)
        
        return await self.after_create(instance)
    
    async def update(self, entity_id: str, data: TUpdate) -> TModel:
        ''' Updates an existing entity in the database.
            - entity_id: The unique identifier of the entity to update.
            - data: The data used to update the entity, typically a Pydantic model or a dictionary.
            - Retrieves the existing entity by ID, converts the input data to a dictionary if it is a Pydantic model, then calls the before_update hook to allow for any custom logic before updating.
            - Uses the repository's update method to persist the changes in the database, then calls the after_update hook to allow for any custom logic after updating before returning the updated instance.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Returns the updated entity instance.
        '''
        instance = await self.get_by_id(entity_id)
        
        payload = data.dict(exclude_unset=True) if hasattr(data, "dict") else data
        
        payload = await self.before_update(instance, payload)
        
        updated = await self.repo.update(entity_id, payload)
        
        return await self.after_update(updated)
    
    async def soft_delete(self, entity_id: str, soft: bool = True) -> None:
        ''' Deletes an entity from the database, either softly or permanently.
            - entity_id: The unique identifier of the entity to delete.
            - soft: A boolean flag indicating whether to perform a soft delete (default: True). If False, performs a hard delete.
            - Retrieves the existing entity by ID, calls the before_delete hook to allow for any custom logic before deletion, then uses the repository's soft_delete or delete method based on the soft flag to remove the entity from the database.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Does not return anything upon successful deletion.
        '''
        instance = await self.get_by_id(entity_id)
        
        await self.before_delete(instance)
        
        return await self.repo.soft_delete(entity_id, soft)
    
    async def delete(self, entity_id: str) -> None:
        ''' Permanently deletes an entity from the database.
            - entity_id: The unique identifier of the entity to delete.
            - Retrieves the existing entity by ID, calls the before_delete hook to allow for any custom logic before deletion, then uses the repository's delete method to permanently remove the entity from the database.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Does not return anything upon successful deletion.
        '''
        instance = await self.get_by_id(entity_id)
        
        await self.before_delete(instance)
        
        return await self.repo.delete(entity_id)