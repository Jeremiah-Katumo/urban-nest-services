from fastapi import Depends, HTTPException, status
from .auth import get_current_user

def require_roles(roles):
    async def checker(data = Depends(get_current_user)):
        user, _ = data
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user
    return checker