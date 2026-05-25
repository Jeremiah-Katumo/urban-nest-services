import math
from sqlalchemy import select, or_, func, desc, asc

class QueryManager:
    ''' Utility class to manage complex query operations such as filtering, sorting, pagination, and response formatting for SQLAlchemy models.
        - apply_columns: Modifies a query to select only specified columns.
        - apply_filters: Adds filtering conditions to a query based on a filter string.
        - apply_sort: Adds sorting to a query based on specified columns and order.
        - paginate: Executes a query with pagination and returns the results along with total count.
        - build_response: Formats the paginated results into a structured response with metadata.
    '''
    
    @staticmethod
    async def apply_columns(stmt, model, columns: str | None):
        ''' Modifies a query to select only specified columns.
            - stmt: The SQLAlchemy query statement to modify.
            - model: The SQLAlchemy model class to reference for column attributes.
            - columns: A string of column names separated by "-", or "all" to select all columns.
            - Returns the modified query statement with only the specified columns selected.
        '''
        if columns and columns != "all":
            selected = []
            for col in columns.split("-"):
                if hasattr(model, col):
                    selected.append(getattr(model, col))
                    
            if selected:
                stmt = stmt.with_only_columns(selected, maintain_column_froms=True)
                
        return stmt
    
    @staticmethod
    async def apply_filters(stmt, model, filter_str: str | None):
        ''' Adds filtering conditions to a query based on a filter string.
            - stmt: The SQLAlchemy query statement to modify.
            - model: The SQLAlchemy model class to reference for column attributes.
            - filter_str: A string of filter criteria separated by "-".
            - Returns the modified query statement with filtering conditions applied.
        '''
        if not filter_str or filter_str == "null":
            return stmt

        criteria = dict(x.split("*") for x in filter_str.split("-"))

        filters = []
        for attr, value in criteria.items():
            if hasattr(model, attr):
                column_attr = getattr(model, attr)
                filters.append(column_attr.ilike(f"%{value}%"))
                
        if filters:
            stmt = stmt.where(or_(*filters))
            
        return stmt
    
    @staticmethod
    async def apply_sort(stmt, model, sort: str | None, order: str = "asc"):
        ''' Adds sorting to a query based on specified columns and order.
            - stmt: The SQLAlchemy query statement to modify.
            - model: The SQLAlchemy model class to reference for column attributes.
            - sort: A string of column names separated by "-" to sort by.
            - order: The sorting order, either "asc" or "desc".
            - Returns the modified query statement with sorting applied.
        '''
        if not sort or sort == "null":
            return stmt
        
        # Validate order        
        order = order.lower()
        if order not in ("asc", "desc"):
            order = "asc"
            
        sorted_columns = []
        for col in sort.split("-"):
            if hasattr(model, col):
                column = getattr(model, col)
                
                if order == "desc":
                    sorted_columns.append(desc(column))
                else:
                    sorted_columns.append(asc(column))
        
        if sorted_columns:
            stmt = stmt.order_by(*sorted_columns)
            
        return stmt

    @staticmethod
    async def paginate(db_session, stmt, page: int, limit: int):
        ''' Executes a query with pagination and returns the results along with total count.
            - db_session: The database session to execute the query.
            - stmt: The SQLAlchemy query statement to execute.
            - page: The page number for pagination (1-based index).
            - limit: The number of items per page for pagination.
            - Returns a tuple containing the query result and the total count of items matching the query.
        '''
        # Clone query WITHOUT limit/offset
        count_stmt = stmt.order_by(None)

        count_stmt = select(func.count()).select_from(
            count_stmt.subquery()
        )

        total = (await db_session.execute(count_stmt)).scalar()

        offset = (page - 1) * limit

        stmt = stmt.offset(offset).limit(limit)

        result = await db_session.execute(stmt)

        return result, total
    
    @staticmethod
    async def build_response(items, page, limit, total):
        ''' Formats the paginated results into a structured response with metadata.
            - items: The list of items retrieved for the current page.
            - page: The current page number.
            - limit: The number of items per page.
            - total: The total number of items matching the query across all pages.
            - Returns a dictionary containing the items and pagination metadata including total pages.
        '''
        total_pages = math.ceil(total / limit)
        
        return {
            "items": items, 
            "page": page, 
            "total": total,
            "pages": total_pages,
            "page_size": limit
        }