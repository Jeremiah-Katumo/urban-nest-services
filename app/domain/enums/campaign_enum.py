from enum import Enum

    
class CampaignStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    EXPIRED = "expired"
    CANCELLED = "cancelled"