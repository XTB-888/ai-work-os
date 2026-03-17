"""
Database utilities for pagination and query optimization.
"""
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = 1
    page_size: int = 20
    
    @property
    def offset(self) -> int:
        """Calculate offset from page and page_size."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


async def paginate(
    db: AsyncSession,
    query: Select,
    params: PaginationParams,
    response_model: type = None
) -> PaginatedResponse:
    """
    Paginate a SQLAlchemy query.
    
    Args:
        db: Database session
        query: SQLAlchemy select query
        params: Pagination parameters
        response_model: Optional Pydantic model for items
        
    Returns:
        PaginatedResponse with items and pagination info
    """
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated items
    paginated_query = query.offset(params.offset).limit(params.page_size)
    result = await db.execute(paginated_query)
    items = result.scalars().all()
    
    # Convert to response model if provided
    if response_model:
        items = [response_model.model_validate(item) for item in items]
    
    # Calculate pagination info
    total_pages = (total + params.page_size - 1) // params.page_size
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
        has_next=params.page < total_pages,
        has_prev=params.page > 1,
    )


class QueryOptimizer:
    """Query optimization utilities."""
    
    @staticmethod
    def add_eager_loading(query: Select, *relationships) -> Select:
        """
        Add eager loading for relationships.
        
        Args:
            query: SQLAlchemy query
            *relationships: Relationship attributes to eager load
            
        Returns:
            Query with eager loading
        """
        from sqlalchemy.orm import selectinload
        
        for rel in relationships:
            query = query.options(selectinload(rel))
        
        return query
    
    @staticmethod
    def add_filters(query: Select, model, filters: dict) -> Select:
        """
        Add filters to query dynamically.
        
        Args:
            query: SQLAlchemy query
            model: SQLAlchemy model
            filters: Dictionary of field: value filters
            
        Returns:
            Query with filters applied
        """
        for field, value in filters.items():
            if hasattr(model, field) and value is not None:
                query = query.where(getattr(model, field) == value)
        
        return query
    
    @staticmethod
    def add_search(query: Select, model, search_fields: List[str], search_term: str) -> Select:
        """
        Add search across multiple fields.
        
        Args:
            query: SQLAlchemy query
            model: SQLAlchemy model
            search_fields: List of field names to search
            search_term: Search term
            
        Returns:
            Query with search applied
        """
        from sqlalchemy import or_
        
        if not search_term:
            return query
        
        search_conditions = []
        for field in search_fields:
            if hasattr(model, field):
                search_conditions.append(
                    getattr(model, field).ilike(f"%{search_term}%")
                )
        
        if search_conditions:
            query = query.where(or_(*search_conditions))
        
        return query
