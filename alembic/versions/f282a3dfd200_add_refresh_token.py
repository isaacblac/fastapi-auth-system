"""add refresh token

Revision ID: f282a3dfd200
Revises: 98d3782a6a5a
Create Date: 2026-02-18 10:21:41.426956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f282a3dfd200'
down_revision: Union[str, Sequence[str], None] = '98d3782a6a5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
