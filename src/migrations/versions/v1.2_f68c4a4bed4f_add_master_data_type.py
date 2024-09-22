"""v1.2

Revision ID: f68c4a4bed4f
Revises: a437a7be5f09
Create Date: 2024-09-22 16:30:58.525167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f68c4a4bed4f'
down_revision: Union[str, None] = 'a437a7be5f09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'master_data_type',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('code', sa.VARCHAR(30), nullable=False),
        sa.Column('name', sa.VARCHAR(30), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("master_data_type")
