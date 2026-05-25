from fastapi import HTTPException, status
from typing import Generic, Type, TypeVar, List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from ...core import query_manager


TModel = TypeVar("TModel")

class BaseRepository(Generic[TModel]):
    ''' A generic repository class providing common database operations for any SQLAlchemy model.
        - TModel: The type of the SQLAlchemy model that this repository will manage.
        - Provides methods for retrieving, creating, updating, and deleting entities, 
            as well as handling custom fields if a value repository is provided.
    '''
    
    def __init__(
        self, 
        db: AsyncSession, 
        model: Type[TModel], 
        value_repo: Optional["ValueRepository"] = None
    ):
        self.db = db
        self.model = model
        self.value_repo = value_repo
        
    async def get_by_id(self, entity_id: str) -> TModel | None:
        ''' Retrieves an entity by its ID.
            - entity_id: The unique identifier of the entity to retrieve.
            - Returns the entity instance if found, or None if not found.
        '''
        result = await self.db.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        search_filter: str | None,
        sort: str | None,
        relations: List[str] = None
    ):
        ''' Retrieves a paginated list of entities with optional filtering, sorting, and related data loading.
            - page: The page number for pagination (1-based index).
            - limit: The number of items per page for pagination.
            - columns: A string of column names separated by "-" to select specific columns, or "all" to select all columns.
            - search_filter: A string of filter criteria separated by "-" to apply to the query.
            - sort: A string of column names separated by "-" to sort by.
            - relations: A list of related model names to load with the main entity.
            - Returns a paginated response containing the list of entities and metadata.
        '''
        stmt = select(self.model).where(self.model.deleted_at.is_(None))
        
        if relations:
            for rel in relations:
                # stmt = stmt.options(selectinload(rel))
                if hasattr(self.model, rel):
                    stmt = stmt.options(selectinload(getattr(self.model, rel)))
        
        # Apply columns, filters, and sorting using the QueryManager utility
        stmt = await query_manager.QueryManager.apply_columns(stmt, self.model, columns) 
        stmt = await query_manager.QueryManager.apply_filters(stmt, self.model, search_filter) 
        stmt = await query_manager.QueryManager.apply_sort(stmt, self.model, sort) 
        
        result, total = await query_manager.QueryManager.paginate(self.db, stmt, page, limit)

        users = result.scalars().unique().all()
        
        return await query_manager.QueryManager.build_response(users, page, limit, total)
    
    async def create(self, obj) -> TModel:
        ''' Creates a new entity in the database.
            - obj: The data for the new entity, which can be a dictionary, Pydantic model, or an instance of the ORM model.
            - Converts the input data to an instance of the ORM model if necessary, then adds it to the database session, 
                commits the transaction, and refreshes the instance to return it with any generated fields (like ID).
            - Returns the created entity instance.
        '''
        # Convert dict/Pydantic → ORM model
        if not isinstance(obj, self.model):
            if isinstance(obj, dict):  # Assuming dict input is compatible with model constructor
                obj = self.model(**obj)
            elif hasattr(obj, "model_dump"):  # Pydantic v2 models
                obj = self.model(**obj.model_dump())
            elif hasattr(obj, "dict"):  # Pydantic v1 models
                obj = self.model(**obj.dict())
            else:
                raise TypeError("Invalid type for create()")

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)

        return obj
    
    async def update(self, entity_id: str, data: dict) -> TModel:
        ''' Updates an existing entity in the database.
            - entity_id: The unique identifier of the entity to update.
            - data: A dictionary of fields and values to update on the entity.
            - Retrieves the existing entity by ID, updates its fields with the provided data, 
                sets the updated_at timestamp if applicable, commits the transaction, and refreshes the instance before returning it.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Returns the updated entity instance.
        '''
        instance = await self.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
        
        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
                
        if hasattr(instance, "updated_at"):
            instance.updated_at = datetime.now(timezone.utc)
            
        await self.db.commit()
        await self.db.refresh(instance)
        
        return instance
    
    async def soft_delete(self, entity_id: str, soft: bool = False) -> TModel | None:
        ''' Soft deletes an entity by setting its deleted_at timestamp, or hard deletes it from the database.
            - entity_id: The unique identifier of the entity to delete.
            - soft: A boolean flag indicating whether to perform a soft delete (default: False).
            - If soft is True and the model has a deleted_at field, sets the deleted_at timestamp to the current time. Otherwise, deletes the entity from the database.
            - Commits the transaction after performing the delete operation.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Returns the deleted entity instance if soft deleted, or None if hard deleted.
        '''
        instance = await self.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
            
        if soft and hasattr(instance, "deleted_at"):
            instance.deleted_at = datetime.now(timezone.utc)
        else:
            self.db.delete(instance)
            
        await self.db.commit()
        
        return instance
    
    async def delete(self, entity_id: str) -> TModel:
        ''' Permanently deletes an entity from the database.
            - entity_id: The unique identifier of the entity to delete.
            - Retrieves the existing entity by ID, deletes it from the database, commits the transaction, and returns the deleted instance.
            - If the entity is not found, raises a 404 Not Found HTTP exception.
            - Returns the deleted entity instance.
        '''
        instance = await self.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
            
        await self.db.delete(instance)
        await self.db.flush()
        
        return instance
        
    async def create_with_custom_fields(self, obj, custom_fields: List[Dict] = None):
        ''' Creates a new entity with associated custom fields.
            - obj: The data for the new entity, which can be a dictionary, Pydantic model, or an instance of the ORM model.
            - custom_fields: A list of dictionaries representing the custom fields to associate with the new entity.
            - Creates the main entity using the create() method, then iterates over the custom fields and creates associated records in the value repository if it is available.
            - Returns the created entity instance.
        '''
        entity = await self.create(obj)

        if custom_fields and self.value_repo:
            for field in custom_fields:
                await self.value_repo.create({
                    "field_id": field["field_id"],
                    "entity_id": entity.id,
                    "module": self.model.__tablename__,
                    "value": field["value"]
                })

        return entity

    async def update_with_custom_fields(
        self, 
        entity_id: str, 
        data: dict, 
        custom_fields: List[Dict] = None
    ) -> TModel:
        ''' Updates an existing entity along with its associated custom fields.
            - entity_id: The unique identifier of the entity to update.
            - data: A dictionary of fields and values to update on the main entity.
            - custom_fields: A list of dictionaries representing the custom fields to update or create for the entity.
            - Updates the main entity using the update() method, then iterates over the custom fields and updates existing records or creates new ones in the value repository if it is available.
            - Returns the updated entity instance.
        '''
        
        entity = await self.update(entity_id, data)

        if custom_fields and self.value_repo:
            existing_values = await self.value_repo.get_by_entity(
                self.model.__tablename__, entity_id
            )

            existing_map = {value.field_id: value for value in existing_values}

            for field in custom_fields:
                if field["field_id"] in existing_map:
                    await self.value_repo.update(
                        existing_map[field["field_id"]].id,
                        {"value": field["value"]}
                    )
                else:
                    await self.value_repo.create({
                        "module": self.model.__tablename__,
                        "entity_id": entity_id,
                        "field_id": field["field_id"],
                        "value": field["value"]
                    })

        return entity

    async def get_custom_fields(self, module: str, entity_id: str):
        ''' Retrieves custom fields associated with a specific entity.
            - module: The name of the module (table) the entity belongs to.
            - entity_id: The unique identifier of the entity for which to retrieve custom fields.
            - If the value repository is available, queries it for custom fields matching the
                module and entity_id, and returns the list of custom field values. Otherwise, 
                returns an empty list.
            - Returns a list of custom field values associated with the specified entity.
        '''
        if not self.value_repo:
            return []
        return await self.value_repo.get_by_entity(module, entity_id)