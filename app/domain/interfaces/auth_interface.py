from abc import ABC, abstractmethod


class IAuth(ABC):
    ''' Interface for authentication-related operations.
        - Defines the contract for authentication repositories, specifying the methods that must be implemented for user registration, authentication, and password reset.
        - This interface allows for different implementations of the authentication repository, enabling flexibility and separation of concerns in the application's architecture.
    '''
    @abstractmethod
    async def register(self, data):
        ''' Registers a new user.
            - data: A RegisterSchema object containing the user's registration information (e.g., email, password, name).
            - This method should create a new user in the database and return the created user object.
        '''
        raise NotImplementedError
    
    @abstractmethod
    async def authenticate(self, plain: str, password: str):
        ''' Authenticates a user.
            - plain: The user's email or username.
            - password: The user's password.
            - This method should verify the user's credentials and return the authenticated user object if successful, or raise an exception if not.
        '''
        raise NotImplementedError
    
    @abstractmethod
    async def reset_password(self, user_id: str, password: str):
        ''' Resets a user's password.
            - user_id: The ID of the user whose password needs to be reset.
            - password: The new password for the user.
            - This method should update the user's password in the database and return the updated user object.
        '''
        raise NotImplementedError
