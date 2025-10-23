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

@router.delete(
    '/{categoria_id}',
    summary='Deletar uma categoria pelo ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DataBaseDependency) -> None:
    categoria: CategoriaModel = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada com o ID {id}.')

    await db_session.delete(categoria)
    await db_session.commit()

@router.patch(
    '/{categoria_id}',
    summary='Editar uma categoria pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada com o ID {id}.')

    elif categoria_in.nome and categoria_in.nome == categoria.nome:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='O nome da categoria não pode ser o mesmo.')

    categoria_update = categoria_in.model_dump(exclude_unset=True)
    for key, value in categoria_update.items():
        setattr(categoria, key, value)

    await db_session.commit()
    await db_session.refresh(categoria)

    return categoria