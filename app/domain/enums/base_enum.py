from enum import Enum

class BaseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"