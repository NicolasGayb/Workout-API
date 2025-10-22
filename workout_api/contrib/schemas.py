from typing import Annotated
from datetime import datetime
from uuid import UUID
from pydantic import UUID4, BaseModel, Field

class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True

class OutMixIn(BaseSchema):
    id: Annotated[UUID4, Field(description="Identificador único", example="123e4567-e89b-12d3-a456-426614174000")]
    created_at: Annotated[datetime, Field(description="Data de criação", example="2023-01-01T00:00:00Z")]
        