"""add transporter_id foreign key in users table

Revision ID: 4a51dbd83f39
Revises: e0e205de6e7e
Create Date: 2026-04-12 01:33:38.924095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sqla
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4a51dbd83f39'
down_revision: Union[str, Sequence[str], None] = 'e0e205de6e7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Fix user_id type
    op.alter_column(
        'support_tickets',
        'user_id',
        existing_type=mysql.INTEGER(),
        type_=sqla.String(length=36),
        nullable=True
    )

    # Create FK
    op.create_foreign_key(
        'fk_support_tickets_user_id_users',
        'support_tickets',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Add transporter_id
    op.add_column('users', sqla.Column('transporter_id', sqla.String(length=36), nullable=True))

    op.create_foreign_key(
        'fk_users_transporter_id',
        'users',
        'transporters',
        ['transporter_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'transporter_id')
    op.drop_constraint(None, 'support_tickets', type_='foreignkey')
    op.alter_column('support_tickets', 'user_id',
               existing_type=sqla.String(length=36),
               type_=mysql.INTEGER(),
               nullable=False)
