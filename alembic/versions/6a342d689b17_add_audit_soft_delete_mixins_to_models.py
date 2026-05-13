"""add audit + soft delete mixins to models

Revision ID: 6a342d689b17
Revises: 49a1d4103c26
Create Date: 2026-05-11 13:06:56.903157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '6a342d689b17'
down_revision: Union[str, Sequence[str], None] = '49a1d4103c26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name, column_name):
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def add_column_if_not_exists(table, column_sql):
    op.execute(f"""
    ALTER TABLE {table}
    ADD COLUMN IF NOT EXISTS {column_sql}
    """)


def add_audit_columns(table_name):
    if not column_exists(table_name, "created_at"):
        op.add_column(table_name, sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))

    if not column_exists(table_name, "updated_at"):
        op.add_column(table_name, sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))

    if not column_exists(table_name, "deleted_at"):
        op.add_column(table_name, sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))

    if not column_exists(table_name, "created_by"):
        op.add_column(table_name, sa.Column("created_by", sa.String(36), nullable=True))
        op.create_foreign_key(
            f"fk_{table_name}_created_by",
            table_name,
            "users",
            ["created_by"],
            ["id"],
            ondelete="SET NULL",
        )

    if not column_exists(table_name, "updated_by"):
        op.add_column(table_name, sa.Column("updated_by", sa.String(36), nullable=True))
        op.create_foreign_key(
            f"fk_{table_name}_updated_by",
            table_name,
            "users",
            ["updated_by"],
            ["id"],
            ondelete="SET NULL",
        )

    if not column_exists(table_name, "deleted_by"):
        op.add_column(table_name, sa.Column("deleted_by", sa.String(36), nullable=True))
        op.create_foreign_key(
            f"fk_{table_name}_deleted_by",
            table_name,
            "users",
            ["deleted_by"],
            ["id"],
            ondelete="SET NULL",
        )


def drop_audit_columns(table_name):
    op.drop_constraint(f"fk_{table_name}_created_by", table_name, type_="foreignkey")
    op.drop_constraint(f"fk_{table_name}_updated_by", table_name, type_="foreignkey")
    op.drop_constraint(f"fk_{table_name}_deleted_by", table_name, type_="foreignkey")

    if column_exists(table_name, "created_by"):
        op.drop_column(table_name, "created_by")
    if column_exists(table_name, "updated_by"):
        op.drop_column(table_name, "updated_by")
    if column_exists(table_name, "deleted_by"):
        op.drop_column(table_name, "deleted_by")

    if column_exists(table_name, "created_at"):
        op.drop_column(table_name, "created_at")
    if column_exists(table_name, "updated_at"):
        op.drop_column(table_name, "updated_at")
    if column_exists(table_name, "deleted_at"):
        op.drop_column(table_name, "deleted_at")


# 👇 Apply to all tables using BaseModelMixin
tables = [
    "permissions",
    "roles",
    "tenants",
    "landlords",
    "agents",
    "transporters",
    "users",
    "properties",
    "campaigns",
    "bookings",
    "features",
    "entities",
    "fields",
    "values",
    "subscriptions",
    "support_tickets",
]


def upgrade():
    for table in tables:
        add_column_if_not_exists(table, "created_at DATETIME NULL")
        add_column_if_not_exists(table, "updated_at DATETIME NULL")
        add_column_if_not_exists(table, "deleted_at DATETIME NULL")

        add_column_if_not_exists(table, "created_by CHAR(36) NULL")
        add_column_if_not_exists(table, "updated_by CHAR(36) NULL")
        add_column_if_not_exists(table, "deleted_by CHAR(36) NULL")

        op.create_foreign_key(
            f"fk_{table}_created_by",
            table,
            "users",
            ["created_by"],
            ["id"],
            ondelete="SET NULL",
        )
        op.create_foreign_key(
            f"fk_{table}_updated_by",
            table,
            "users",
            ["updated_by"],
            ["id"],
            ondelete="SET NULL",
        )
        op.create_foreign_key(
            f"fk_{table}_deleted_by",
            table,
            "users",
            ["deleted_by"],
            ["id"],
            ondelete="SET NULL",
        )

    # Only if it REALLY exists in previous schema
    op.drop_column("user_permissions", "created_at")
    op.drop_column("user_permissions", "updated_at")
    op.drop_column("user_permissions", "deleted_at")


def downgrade():
    for table in tables:
        op.drop_constraint(f"fk_{table}_created_by", table, type_="foreignkey")
        op.drop_constraint(f"fk_{table}_updated_by", table, type_="foreignkey")
        op.drop_constraint(f"fk_{table}_deleted_by", table, type_="foreignkey")

        op.drop_column(table, "created_by")
        op.drop_column(table, "updated_by")
        op.drop_column(table, "deleted_by")

        op.drop_column(table, "created_at")
        op.drop_column(table, "updated_at")
        op.drop_column(table, "deleted_at")