from typing import List
from .base_usecase import BaseUseCase
from ...models.models import FieldModel


class FieldUseCase(BaseUseCase):
    
    async def get_all_by_module(self, module: str) -> List[FieldModel]:
        return await self.repo.get_all_by_module(module)
