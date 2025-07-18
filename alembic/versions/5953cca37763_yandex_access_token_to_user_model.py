"""yandex-access-token-to-user-model

Revision ID: 5953cca37763
Revises: 2e0a4adc38cb
Create Date: 2025-06-24 15:59:58.858906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5953cca37763'
down_revision: Union[str, None] = '2e0a4adc38cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserProfile', sa.Column('yandex_access_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserProfile', 'yandex_access_token')
    # ### end Alembic commands ###
