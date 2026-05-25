from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from ...domain.interfaces.auth_interface import IAuth
from ...models.models import UserModel
from ...core.security import hash_password, verify_password
from ...infrastructure.repositories.user_repository import UserRepository


class AuthRepository(IAuth):
    ''' Repository class for authentication-related database operations.
        - Implements the IAuth interface, providing concrete implementations for user registration, authentication, and password reset.
        - Interacts with the database using SQLAlchemy's AsyncSession to perform CRUD operations on the UserModel.
    '''
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)

    async def register(self, data):
        ''' Registers a new user in the database.
            - data: A RegisterSchema object containing the user's registration information (username, first name, last name, email, phone, password, role).
            - Checks if a user with the provided email already exists in the database. If a user exists, raises a 400 Bad Request HTTP exception with a "User Exists" message.
            - If the email is unique, creates a new UserModel instance with the provided data, hashing the password before storing it.
            - Adds the new user to the database session, commits the transaction, and refreshes the session to retrieve the newly created user object.
            - Returns the newly created user object.
        '''
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.email == data.email,
                UserModel.deleted_at.is_(None)
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Exists"
            )

        user = UserModel(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password),
            role=data.role,
            created_at=datetime.now(timezone.utc)
        )

        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def authenticate(self, email: str, password: str):
        ''' Authenticates a user based on their email and password.
            - email: The email address of the user attempting to authenticate.
            - password: The plaintext password provided by the user for authentication.
            - Retrieves the user from the database using the provided email address.
            - If the user does not exist, raises a 404 Not Found HTTP exception with a "User not found" message.
            - If the user exists, verifies the provided password against the stored hashed password using the verify_password function.
            - If the password verification fails, raises a 401 Unauthorized HTTP exception with an "Authentication Error!" message.
            - If the password verification is successful, returns the user object.
        '''
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(404, "User not found")
        
        if not verify_password(password, user.password):
            raise HTTPException(401, "Authentication Error!")

        return user

    async def reset_password(self, user_id: str, password: str):
        ''' Resets the password for a user.
            - user_id: The ID of the user whose password is to be reset.
            - password: The new password to be set for the user.
            - Retrieves the user from the database using the provided user_id.
            - If the user does not exist, raises a 404 Not Found HTTP exception with a "User does not exist" message.
            - If the user exists, hashes the new password and updates the user's password in the database.
            - Commits the transaction and returns a success message indicating that the password reset was successful.
        '''
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.id == user_id,
                UserModel.deleted_at.is_(None)
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User does not exist")

        user.password = hash_password(password)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return {"message": "Password reset successful"}