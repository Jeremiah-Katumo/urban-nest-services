import enum

class UserRole(str, enum.Enum):
    TENANT = "TENANT"
    LANDLORD = "LANDLORD"
    AGENT = "AGENT"

class TicketStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    IN_PROGRESS = "IN_PROGRESS"

class TicketCategory(str, enum.Enum):
    PAYMENT = "PAYMENT"
    BOOKING = "BOOKING"
    MAINTENANCE = "MAINTENANCE"
    OTHER = "OTHER"