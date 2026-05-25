from .base_usecase import BaseUseCase
from ..interfaces.campaign_interface import ICampaign

class CampaignUseCase(BaseUseCase):
    
    def __init__(self, repo: ICampaign, response_schema=None):
        super().__init__(repo, response_schema)