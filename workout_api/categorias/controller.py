from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DataBaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
        path='/', 
        summary='Criar nova categoria', 
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut
)

async def post(
    db_session: DataBaseDependency, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:

    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out

@router.get(
    '/',
    summary='Listar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(db_session: DataBaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()

    if not categorias:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhuma categoria encontrada.')
    return categorias

@router.get(
    '/{categoria_id}',
    summary='Listar uma categoria pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada com o ID {id}.')
    return categoria