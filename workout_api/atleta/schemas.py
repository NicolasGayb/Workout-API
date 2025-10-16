from pydantic import BaseModel, Field
from typing import Annotated

class Atleta(BaseModel):
    nome: Annotated[str, Field(description="Nome do atleta", example="João Silva", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", example=1.75)]
    genero: Annotated[str, Field(description="Gênero do atleta", example="M", max_length=1)]