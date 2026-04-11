from enum import Enum


class PermissionEnum(str, Enum):
    GENERATE_DESCRIPTION = "generate_description"
    CREATE_CAMPAIGN = "create_campaign"
    EDIT_CAMPAIGN = "edit_campaign"
    VIEW_CAMPAIGN = "view_campaign"
    MANAGE_PRODUCTS = "manage_products"