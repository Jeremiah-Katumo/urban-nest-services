from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.user_entity import UserRead, UserCreate
from ..infrastructure.db.database import db
from ..domain.usecases.user_usecase import UserUseCase
from ..infrastructure.repositories.user_repository import UserRepository
from ..models.models import UserModel

router = APIRouter()

@router.post("/", response_model=UserRead)
async def get_all(
    skip: int,
    limit: int,
    search: str,
    sort_by: str,
    order: str, 
    db: AsyncSession = Depends(db.get_db)
):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    users = await use_case.get_all(skip, limit, search, sort_by, order)
    return users

@router.get("/{id}", response_model=UserRead)
async def get_by_id(id: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_id(id)
    return user

@router.get("/{email}", response_model=UserRead)
async def get_by_id(email: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_email(email)
    return user

@router.get("/{username}", response_model=UserRead)
async def get_by_id(username: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_username(username)
    return user