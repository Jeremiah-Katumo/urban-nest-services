from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.user_entity import UserRead, UserCreate
from ..infrastructure.db.database import db
from ..domain.usecases.user_usecase import UserUseCase
from ..infrastructure.repositories.user_repository import UserRepository
from ..models.models import UserModel

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(db.get_db)):
    user = UserModel(**user_data.model_dump())
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    new_user = await use_case.create(user_data)
    return new_user

@router.get("/{id}", response_model=UserRead)
async def get_by_id(id: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_id(id)
    return user