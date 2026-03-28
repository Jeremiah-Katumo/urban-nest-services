"""add entity_id foreign keys

Revision ID: 7f89cce44630
Revises: 271730d7c2b7
Create Date: 2026-03-28 08:33:38.014535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '7f89cce44630'
down_revision: Union[str, Sequence[str], None] = '271730d7c2b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name, column_name):
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    tables = [
        "users",
        "tenants",
        "landlords",
        "agents",
        "properties",
        "campaigns",
        "features",
        "permissions",
        "roles",
    ]

    for table in tables:
        if not column_exists(table, "entity_id"):
            op.add_column(table, sa.Column("entity_id", sa.String(length=36), nullable=True))

        # Create FK only if needed (MySQL safe approach = try/except)
        try:
            op.create_foreign_key(
                f"fk_{table}_entity_id",
                table,
                "entities",
                ["entity_id"],
                ["id"],
                ondelete="CASCADE",
            )
        except Exception:
            pass

def downgrade():
    # Reverse order (important for FK dependencies)

    op.drop_constraint("fk_roles_entity_id", "roles", type_="foreignkey")
    op.drop_column("roles", "entity_id")

    op.drop_constraint("fk_permissions_entity_id", "permissions", type_="foreignkey")
    op.drop_column("permissions", "entity_id")

    op.drop_constraint("fk_features_entity_id", "features", type_="foreignkey")
    op.drop_column("features", "entity_id")

    op.drop_constraint("fk_campaigns_entity_id", "campaigns", type_="foreignkey")
    op.drop_column("campaigns", "entity_id")

    op.drop_constraint("fk_properties_entity_id", "properties", type_="foreignkey")
    op.drop_column("properties", "entity_id")

    op.drop_constraint("fk_agents_entity_id", "agents", type_="foreignkey")
    op.drop_column("agents", "entity_id")

    op.drop_constraint("fk_landlords_entity_id", "landlords", type_="foreignkey")
    op.drop_column("landlords", "entity_id")

    op.drop_constraint("fk_tenants_entity_id", "tenants", type_="foreignkey")
    op.drop_column("tenants", "entity_id") 

    op.drop_constraint("fk_users_entity_id", "users", type_="foreignkey")
    op.drop_column("users", "entity_id")
    