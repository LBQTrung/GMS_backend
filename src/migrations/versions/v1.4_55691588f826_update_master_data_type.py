"""v1.4

Revision ID: 55691588f826
Revises: a4733a36ddf1
Create Date: 2024-09-24 10:35:42.597365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55691588f826'
down_revision: Union[str, None] = 'a4733a36ddf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("master_data_code_fkey", "master_data", type_='foreignkey')
    op.drop_constraint("uq_master_data_type_code", "master_data_type", type_='unique')


def downgrade() -> None:
    op.create_unique_constraint("uq_master_data_type_code", "master_data_type", ["code"])
    op.create_foreign_key("master_data_code_fkey", "master_data", "master_data_type", ["code"], ["code"], ondelete='CASCADE')

