from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timezone, timedelta
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # Default to 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))  # Default to 7 days

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    ''' Hashes a plain password using Passlib's CryptContext.
        - Uses the configured hashing algorithm (Argon2 in this case) to hash the password.
        - Returns the hashed password as a string.
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    ''' Verifies a plain password against a hashed password.
        - Uses Passlib's verify function to check if the plain password matches the hashed password.
        - Returns True if the password is correct, False otherwise.
    '''
    return pwd_context.verify(plain_password, hashed_password)

def verify_and_update(plain_password: str, hashed_password: str):
    ''' Verifies the password and updates the hash if needed.
        - Uses Passlib's verify_and_update to check if the password is correct and if the hash needs to be updated (e.g., if the hashing algorithm has changed).
        - Returns a tuple (is_valid, new_hash) where is_valid indicates if the password is correct and new_hash is the updated hash if it was updated, or None if no update is needed.
    '''
    return pwd_context.verify_and_update(plain_password, hashed_password)

def create_access_token(user_id: str, role: str):
    ''' Creates a JWT access token with user ID, role, and expiration.
        - Uses a unique JTI for token revocation support.
        - Encodes the token with the configured secret key and algorithm.
    '''
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str):
    ''' Creates a JWT refresh token with user ID and expiration.
        - Uses a unique JTI for token revocation support.
        - Encodes the token with the configured secret key and algorithm.
    '''
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": str(uuid.uuid4()),
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # ✅ FIXED
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)