from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.models import PermissionModel, RoleModel
from ..domain.enums.permission_enum import PermissionEnum
from ..infrastructure.db.database import db as async_session


async def seed_permissions(db: AsyncSession):
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


roles_permissions_map = {
    "admin": ["create_user", "delete_user", "update_user", "generate_description"],
    "super_admin": ["*"],  # '*' = all permissions
    "manager": ["generate_description", "view_reports"],
    "agent": ["view_properties", "create_booking"],
    "tenant": ["view_properties", "create_booking"]
}

permissions_descriptions = {
    "create_user": "Ability to create a user",
    "delete_user": "Ability to delete a user",
    "update_user": "Ability to update a user",
    "generate_description": "Ability to generate descriptions using AI",
    "view_reports": "Ability to view system reports",
    "view_properties": "Ability to view properties",
    "create_booking": "Ability to create a booking",
    "*": "Full access to all permissions"
}


async def seed_roles_permissions():
    async with async_session.get_session() as session:
        async with session.begin():
            # Seed permissions
            for perm_name, desc in permissions_descriptions.items():
                existing_perm = await session.execute(
                    select(PermissionModel).where(
                        PermissionModel.name == perm_name
                    )
                )
                perm = existing_perm.scalar_one_or_none()
                if not perm:
                    perm = PermissionModel(name=perm_name, description=desc)
                    session.add(perm)
            
            await session.flush()  # flush so permissions have IDs

            # Seed roles
            for role_name, perms in roles_permissions_map.items():
                existing_role = await session.execute(select(RoleModel).where(RoleModel.name == role_name))
                role = existing_role.scalar_one_or_none()
                if not role:
                    role = RoleModel(name=role_name, description=f"{role_name} role")
                    session.add(role)
                    await session.flush()
                
                # Attach permissions to role
                role.permissions = []
                for perm_name in perms:
                    if perm_name == "*":
                        all_perms = await session.execute(select(PermissionModel))
                        role.permissions = all_perms.scalars().all()
                        break
                    perm = await session.execute(
                        select(PermissionModel).where(
                            PermissionModel.name == perm_name
                        )
                    )
                    perm_obj = perm.scalar_one_or_none()
                    if perm_obj:
                        role.permissions.append(perm_obj)

            await session.commit()
            print("Roles and permissions seeded successfully!")
            