from typing import Annotated
from pydantic import UUID4, Field

from workout_api.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Força", max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="ID da categoria", example="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
