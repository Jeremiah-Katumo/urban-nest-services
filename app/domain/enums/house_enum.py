from enum import Enum


class HouseStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
