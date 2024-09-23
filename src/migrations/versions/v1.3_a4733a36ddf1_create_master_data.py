"""v1.3

Revision ID: a4733a36ddf1
Revises: f68c4a4bed4f
Create Date: 2024-09-23 20:35:31.100686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4733a36ddf1'
down_revision: Union[str, None] = 'f68c4a4bed4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("master_data_type", "code", nullable=False)
    op.create_unique_constraint("uq_master_data_type_code", "master_data_type", ["code"])

    op.create_table(
        'master_data',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('code', sa.VARCHAR(30), nullable=False),
        sa.Column('name', sa.VARCHAR(30), nullable=False),
        sa.Column('value', sa.VARCHAR(20), nullable=True),
        sa.Column('data', sa.JSON, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['code'], ['master_data_type.code'], ondelete='CASCADE'),
    )



def downgrade() -> None:
    op.drop_table("master_data")

    op.drop_constraint("uq_master_data_type_code", "master_data_type", type_='unique')
    op.alter_column("master_data_type", "code", nullable=False)
    

