"""add organization content fields to entities

Revision ID: 76cf6873c7fd
Revises: 6a9375e32b3c
Create Date: 2026-05-25 12:11:06.298984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76cf6873c7fd'
down_revision: Union[str, Sequence[str], None] = '6a9375e32b3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("entities") as batch_op:
        batch_op.add_column(sa.Column("entity_heading", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("hero_section", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("about", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("mission", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("vision", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("motto", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("contacts", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("footer", sa.JSON(), nullable=True))


def downgrade():
    with op.batch_alter_table("entities") as batch_op:
        batch_op.drop_column("footer")
        batch_op.drop_column("contacts")
        batch_op.drop_column("motto")
        batch_op.drop_column("vision")
        batch_op.drop_column("mission")
        batch_op.drop_column("about")
        batch_op.drop_column("hero_section")
        batch_op.drop_column("entity_heading")
