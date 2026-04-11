"""add pricing and status fields to transporters

Revision ID: e0e205de6e7e
Revises: 8ba9e6a4e0f8
Create Date: 2026-04-11 14:03:53.146540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0e205de6e7e'
down_revision: Union[str, Sequence[str], None] = '8ba9e6a4e0f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns
    op.add_column("transporters", sa.Column("base_price", sa.Float(), nullable=False, server_default="50"))
    op.add_column("transporters", sa.Column("price_per_km", sa.Float(), nullable=False, server_default="2"))
    op.add_column("transporters", sa.Column("rating", sa.Float(), nullable=False, server_default="4.7"))

    # Enum type (MySQL compatible)
    driver_status_enum = sa.Enum("AVAILABLE", "BUSY", "OFFLINE", name="driverstatusenum")
    driver_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "transporters",
        sa.Column("driver_status", driver_status_enum, nullable=False, server_default="AVAILABLE")
    )


def downgrade():
    op.drop_column("transporters", "driver_status")
    op.drop_column("transporters", "rating")
    op.drop_column("transporters", "price_per_km")
    op.drop_column("transporters", "base_price")

    sa.Enum(name="driverstatusenum").drop(op.get_bind(), checkfirst=True)