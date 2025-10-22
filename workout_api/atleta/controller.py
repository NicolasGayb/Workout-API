from fastapi import APIRouter, status

router = APIRouter()

@router.post(
        path='/', 
        summary='Criar novo atleta', 
        status_code=status.HTTP_201_CREATED
        )

async def post():
    pass