"""add user role

Revision ID: 8a3d2f1b6c4e
Revises: 6cd816b26a2b
Create Date: 2026-07-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8a3d2f1b6c4e"
down_revision: Union[str, None] = "6cd816b26a2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(length=50), nullable=False, server_default="member"),
    )
    op.alter_column("users", "role", server_default=None, existing_type=sa.String(length=50))


def downgrade() -> None:
    op.drop_column("users", "role")
