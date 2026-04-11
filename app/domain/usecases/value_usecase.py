from typing import List
from .base_usecase import BaseUseCase
from ...models.models import ValueModel


class ValueUseCase(BaseUseCase):
    
    async def get_by_entity(self, module: str, entity_id: str) -> List[ValueModel]:
        return await self.repo.get_by_entity(module, entity_id)
