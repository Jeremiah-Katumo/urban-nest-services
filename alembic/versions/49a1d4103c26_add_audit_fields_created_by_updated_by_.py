"""add audit fields (created_by, updated_by, deleted_by)

Revision ID: 49a1d4103c26
Revises: 4a51dbd83f39
Create Date: 2026-05-11 08:49:13.998569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49a1d4103c26'
down_revision: Union[str, Sequence[str], None] = '4a51dbd83f39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 👇 tables that should have audit fields
TABLES = [
    "users",
    "tenants",
    "landlords",
    "agents",
    "transporters",
    "properties",
    "bookings",
    "features",
    "permissions",
    "roles",
    "entities",
    "fields",
    "values",
    "subscriptions",
    "support_tickets",
    "campaigns",
]


def upgrade():
    for table in TABLES:
        # Add columns
        op.add_column(table, sa.Column("created_by", sa.String(length=36), nullable=True))
        op.add_column(table, sa.Column("updated_by", sa.String(length=36), nullable=True))
        op.add_column(table, sa.Column("deleted_by", sa.String(length=36), nullable=True))

        # Add foreign keys → users.id
        op.create_foreign_key(
            f"fk_{table}_created_by",
            source_table=table,
            referent_table="users",
            local_cols=["created_by"],
            remote_cols=["id"],
            ondelete="SET NULL",
        )

        op.create_foreign_key(
            f"fk_{table}_updated_by",
            source_table=table,
            referent_table="users",
            local_cols=["updated_by"],
            remote_cols=["id"],
            ondelete="SET NULL",
        )

        op.create_foreign_key(
            f"fk_{table}_deleted_by",
            source_table=table,
            referent_table="users",
            local_cols=["deleted_by"],
            remote_cols=["id"],
            ondelete="SET NULL",
        )


def downgrade():
    for table in TABLES:
        # Drop FKs first (IMPORTANT)
        op.drop_constraint(f"fk_{table}_created_by", table, type_="foreignkey")
        op.drop_constraint(f"fk_{table}_updated_by", table, type_="foreignkey")
        op.drop_constraint(f"fk_{table}_deleted_by", table, type_="foreignkey")

        # Drop columns
        op.drop_column(table, "created_by")
        op.drop_column(table, "updated_by")
        op.drop_column(table, "deleted_by")