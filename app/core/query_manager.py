import math
from sqlalchemy import select, or_, func, desc, asc

class QueryManager:
    
    @staticmethod
    async def apply_columns(stmt, model, columns: str | None):
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
        if not sort or sort == "null":
            return stmt
        
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
        total_pages = math.ceil(total / limit)
        
        return {
            "items": items, 
            "page": page, 
            "total": total,
            "pages": total_pages,
            "page_size": limit
        }