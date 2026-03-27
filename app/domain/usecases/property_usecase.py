from fastapi import HTTPException, status
from .base_usecase import BaseUseCase


class PropertyUseCase(BaseUseCase):
    
    async def assign_landlord(self, property_id: str, landlord_id: str):
        prop = await self.get_by_id(property_id)
        
        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Property not found"
            )
            
        return await self.repo.assign_landlord(property_id, landlord_id)
    
    async def assign_agent(self, property_id: str, agent_id: str):
        prop = await self.get_by_id(property_id)
        
        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Property not found"
            )
            
        return await self.repo.assign_agent(property_id, agent_id)