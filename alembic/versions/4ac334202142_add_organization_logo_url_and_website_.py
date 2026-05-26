"""add organization logo_url and website_url fields to entities

Revision ID: 4ac334202142
Revises: 76cf6873c7fd
Create Date: 2026-05-25 12:27:32.775391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ac334202142'
down_revision: Union[str, Sequence[str], None] = '76cf6873c7fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("entities") as batch_op:
        batch_op.add_column(sa.Column("logo_url", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("website_url", sa.String(255), nullable=True))


def downgrade():
    with op.batch_alter_table("entities") as batch_op:
        batch_op.drop_column("logo_url")
        batch_op.drop_column("website_url")