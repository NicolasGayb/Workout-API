from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DataBaseDependency
from sqlalchemy.future import select
from uuid import UUID as _UUID

router = APIRouter()

@router.post(
        path='/', 
        summary='Criar um novo centro de treinamento', 
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut
)

async def post(
    db_session: DataBaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out

@router.get(
    '/',
    summary='Listar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centros: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()

    if not centros:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum centro de treinamento encontrado.')
    return centros

@router.get(
    '/{ct_id}',
    summary='Listar um centro de treinamento pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(ct_id: UUID4, db_session: DataBaseDependency) -> CentroTreinamentoOut:
    centro: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado com o ID {id}.')
    return centro

@router.delete(
    '/{ct_id}',
    summary='Deletar um centro de treinamento pelo ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(ct_id: UUID4, db_session: DataBaseDependency) -> None:
    centro: CentroTreinamentoModel = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=ct_id))).scalars().first()

    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado com o ID {ct_id}.')
    try:
        _UUID(str(ct_id), version=4)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='O ID deve estar no padrão correto (ex: 123e4567-e89b-12d3-a456-426614174000).')

    await db_session.delete(centro)
    await db_session.commit()

@router.patch(
    '/{ct_id}',
    summary='Editar um centro de treinamento pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(ct_id: UUID4, db_session: DataBaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    centro: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=ct_id))).scalars().first()

    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado com o ID {ct_id}.')
    elif centro_treinamento_in.nome and centro_treinamento_in.nome == centro.nome:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='O nome do centro de treinamento não pode ser o mesmo.')
    

    centro_update = centro_treinamento_in.model_dump(exclude_unset=True)
    for key, value in centro_update.items():
        setattr(centro, key, value)

    await db_session.commit()
    await db_session.refresh(centro)

    return centro