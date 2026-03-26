from enum import Enum

    
class LandlordStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"