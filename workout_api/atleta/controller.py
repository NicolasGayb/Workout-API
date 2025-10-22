from sqlite3 import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from datetime import datetime

from fastapi.params import Depends
from fastapi_pagination import LimitOffsetParams
from pydantic import UUID4
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
        path='/', 
        summary='Criar novo atleta', 
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut
)

async def post(
    db_session: DataBaseDependency, 
    atleta_in: AtletaIn = Body(...)
):
    categoria_name = atleta_in.categoria.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_name))
        ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria {categoria_name} não encontrada.'
        )

    centro_treinamento_name = atleta_in.centro_treinamento.nome

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name))
        ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento {centro_treinamento_name} não encontrado.'
        )
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Dados inválidos para criação do atleta.'
        )

    db_session.add(atleta_model)

    try:
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Atleta com CPF {atleta_in.cpf} já existe.'
        )

    return atleta_out

@router.get(
    '/',
    summary='Listar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(
    db_session: DataBaseDependency,
    nome: str | None = Query(default=None, description="Filtrar por nome do atleta"),
    cpf: str | None = Query(default=None, description="Filtrar por CPF do atleta"),
    params: LimitOffsetParams = Depends(LimitOffsetParams),
    ) -> list[dict]:

    stmt = select(AtletaModel).options(
        selectinload(AtletaModel.categoria),
        selectinload(AtletaModel.centro_treinamento)
    )

    if nome:
        stmt = stmt.filter(AtletaModel.nome.ilike(f'%{nome}%'))
    if cpf:
        stmt = stmt.filter(AtletaModel.cpf == cpf)

    stmt = stmt.limit(params.limit).offset(params.offset)

    atletas: list[AtletaModel] = (await db_session.execute(stmt)).scalars().all()

    if not atletas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum atleta encontrado.')
    
    response = []
    for atleta in atletas:
        response.append({
            "nome": getattr(atleta, "nome", None),
            "centro_treinamento": getattr(atleta.centro_treinamento, "nome", None),
            "categoria": getattr(atleta.categoria, "nome", None),
        })
    return response

@router.get(
    '/{id}',
    summary='Listar um atleta pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado com o ID {id}.')
    return atleta

@router.patch(
    '/{id}',
    summary='Editar um atleta pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado com o ID {id}.')

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    try:
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        cpf_value = atleta_update.get('cpf', getattr(atleta, 'cpf', None))
        raise HTTPException(
            status_code=303,
            detail=f'Já existe um atleta cadastrado com o cpf: {cpf_value}'
        )

    await db_session.refresh(atleta)
    
    return atleta

@router.delete(
    '/{id}',
    summary='Deletar um atleta pelo ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado com o ID {id}.')

    await db_session.delete(atleta)
    await db_session.commit()