from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "pending"
    REJECTED = "rejected"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"