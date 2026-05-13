from .base_usecase import BaseUseCase


class TransporterUseCase(BaseUseCase):
    
    def __init__(self, repo, response_schema=None):
        super().__init__(repo, response_schema)