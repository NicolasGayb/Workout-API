from typing import Annotated
from pydantic import UUID4, Field

from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Academia XYZ", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Rua A, 123", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="João da Silva", max_length=30)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento", example="550e8400-e29b-41d4-a716-446655440000")]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Maria Oliveira", max_length=20)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[float, Field(description="Peso do atleta", example=70.5)]
    altura: Annotated[float, Field(description="Altura do atleta", example=1.75)]