from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.models import PermissionModel, RoleModel
from ..domain.enums.permission_enum import PermissionEnum
from ..infrastructure.db.database import db as async_session


async def seed_permissions(db: AsyncSession):
    ''' Seeds the database with predefined permissions.
    
        Arguments: 
            - db: An asynchronous database session used to interact with the database.
            
        Functionality:
        - Retrieves existing permissions from the database to avoid duplicates.
        - Compares existing permissions with the predefined PermissionEnum and creates any missing permissions.
        - Uses transactions to ensure data integrity and prevent duplicates.
        - Designed to be idempotent, allowing safe re-seeding without creating duplicates.
        - Logs progress and results for visibility.
    '''
    result = await db.execute(select(PermissionModel.name))
    existing_permissions = {row(0) for row in result.fetchall()}
    # existing_permissions = set(result.scalars().all())
    
    new_permissions = []
    for permission in PermissionEnum:
        if permission.value not in existing_permissions:
            new_permissions.append(
                PermissionModel(
                    name=permission.value,
                    description=f"Permission for {permission.value.replace('_', ' ').title()}"
                )
            )
            
    if new_permissions:
        db.add_all(new_permissions)
        await db.commit()

# Roles and their associated permissions
roles_permissions_map = {
    "admin": [
        "generate_description", "view_reports", "view_dashboard",
        "manage_properties",
        "manage_bookings",
        "manage_users",
        "manage_campaigns",
        "manage_tenants",
        "manage_landlords",
        "manage_agents",
        "manage_movers",
        "manage_discounts",
        "manage_promotions",
        "manage_content",
        "manage_settings"
    ],
    "super_admin": ["*"],  # '*' = all permissions
    "manager": [
        "generate_description", "view_reports", "view_dashboard",
        "manage_bookings",
        "manage_campaigns",
        "manage_tenants",
        "manage_landlords",
        "manage_agents",
        "manage_movers",
        "manage_discounts",
        "manage_promotions",
        "manage_content",
        "manage_settings",
        "view_user", "update_user", "delete_user",
    ],
    "agent": [
        "view_dashboard",
        "manage_properties", 
        "manage_bookings",
        "manage_campaigns",
        "manage_tenants",
        "manage_landlords",
        "view_user", "update_user", "delete_user",
    ],
    "tenant": [
        "view_properties", 
        "view_bookings", "view_booking", "create_booking", "update_booking", "delete_booking",
        "view_campaigns", "view_campaign"
        "view_user", "update_user", "delete_user",
    ],
    "landlord": [
        "view_dashboard",
        "manage_properties",
        "manage_bookings",
        "manage_campaigns",
        "manage_tenants",
        "manage_agents",
        "view_user", "update_user", "delete_user",
    ],
    "mover": [
        "view_dashboard",
        "manage_bookings",
        "view_campaigns", "view_campaign",
        "view_user", "update_user", "delete_user",
    ],
}

# Permission description for better clarity in the database
permissions_descriptions = {
    "view_users": "Ability to view users",
    "view_user": "Ability to view a single user",
    "create_user": "Ability to create a user",
    "delete_user": "Ability to delete a user",
    "update_user": "Ability to update a user",
    "view_dashboard": "Ability to view dashboard",
    "generate_description": "Ability to generate descriptions using AI",
    "view_reports": "Ability to view system reports",
    "view_properties": "Ability to view properties",
    "view_property": "Ability to view a single property",
    "create_property": "Ability to create property",
    "update_property": "Ability to update property",
    "delete_property": "Ability to delete property",
    "view_bookings": "Ability to view bookings",
    "view_booking": "Ability to view a single booking",
    "create_booking": "Ability to create booking",
    "update_booking": "Ability to update booking",
    "delete_booking": "Ability to delete booking",
    "view_campaigns": "Ability to view campaigns",
    "view_campaign": "Ability to view a single campaign",
    "create_campaign": "Ability to create campaigns",
    "update_campaign": "Ability to edit campaigns",
    "delete_campaign": "Ability to delete campaigns",
    "manage_properties": "Full access to manage properties",
    "manage_bookings": "Full access to manage bookings",
    "manage_users": "Full access to manage users",
    "manage_campaigns": "Full access to manage campaigns",
    "manage_tenants": "Full access to manage tenants",
    "manage_landlords": "Full access to manage landlords",
    "manage_agents": "Full access to manage agents",
    "manage_movers": "Full access to manage movers",
    "manage_discounts": "Full access to manage discounts",
    "manage_promotions": "Full access to manage promotions",
    "manage_content": "Full access to manage content",
    "manage_settings": "Full access to manage settings",
    "*": "Full access to all permissions"
}


async def seed_roles_permissions():
    ''' Seeds the database with predefined roles and permissions. 
        - Creates missing permissions based on PermissionEnum.
        - Creates/updates roles and assigns permissions based on roles_permissions_map.
        - Uses transactions to ensure data integrity and prevent duplicates.
        - Designed to be idempotent, allowing safe re-seeding without creating duplicates.
        - Logs progress and results for visibility.
    '''
    async for session in async_session.get_session():
        async with session.begin():

            # 1. LOAD EXISTING PERMISSIONS
            result = await session.execute(select(PermissionModel))
            existing_permissions = {
                perm.name: perm for perm in result.scalars().all()
            }

            # 2. CREATE MISSING PERMISSIONS
            new_permissions = []
            for perm_name, desc in permissions_descriptions.items():
                if perm_name not in existing_permissions:
                    perm = PermissionModel(name=perm_name, description=desc)
                    session.add(perm)
                    new_permissions.append(perm)

            if new_permissions:
                await session.flush()
                for perm in new_permissions:
                    existing_permissions[perm.name] = perm

            # 3. LOAD EXISTING ROLES
            result = await session.execute(select(RoleModel))
            existing_roles = {
                role.name: role for role in result.scalars().all()
            }

            # 4. CREATE / UPDATE ROLES
            for role_name, perm_names in roles_permissions_map.items():
                role = existing_roles.get(role_name)
                if not role:
                    role = RoleModel(
                        name=role_name,
                        description=f"{role_name} role"
                    )
                    session.add(role)
                    await session.flush()

                # HANDLE "*" (ALL PERMISSIONS)
                # 🔐 ensure relationship is loaded (prevents implicit query)
                await session.refresh(role, ["permissions"])

                # clear existing safely
                role.permissions.clear()

                # assign safely
                if "*" in perm_names:
                    role.permissions.extend(existing_permissions.values())
                else:
                    role.permissions.extend(
                        existing_permissions[p]
                        for p in perm_names
                        if p in existing_permissions
                    )

            print("✅ Roles and permissions seeded successfully!")