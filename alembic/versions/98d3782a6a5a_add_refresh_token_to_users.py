"""add refresh_token to users

Revision ID: 98d3782a6a5a
Revises: 6996c148d943
Create Date: 2026-02-18 07:37:39.851680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98d3782a6a5a'
down_revision: Union[str, Sequence[str], None] = '6996c148d943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column("refresh_token", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "refresh_token")
