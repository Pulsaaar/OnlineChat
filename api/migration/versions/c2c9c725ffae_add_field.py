"""add field

Revision ID: c2c9c725ffae
Revises: e21d62eff22b
Create Date: 2024-10-27 23:30:20.989232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2c9c725ffae'
down_revision: Union[str, None] = 'e21d62eff22b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('telegram_id', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'user', ['telegram_id'])
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'telegram_id')
    # ### end Alembic commands ###
