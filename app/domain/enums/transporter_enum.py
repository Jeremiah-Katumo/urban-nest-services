from enum import Enum

class IntervalEnum(str, Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class RoleEnum(str, Enum):
    LANDLORD = "LANDLORD"
    AGENT = "AGENT"
    TRANSPORTER = "TRANSPORTER"
    

class DriverStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"