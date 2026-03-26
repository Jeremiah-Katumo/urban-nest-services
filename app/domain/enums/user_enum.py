from enum import Enum

    
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    
class UserRoles(str, Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    AGENT = "agent"
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    MANAGER = "manager"
    