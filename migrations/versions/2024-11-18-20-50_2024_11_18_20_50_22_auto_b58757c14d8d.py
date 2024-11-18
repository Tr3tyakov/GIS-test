"""2024-11-18_20-50-22-auto

Revision ID: b58757c14d8d
Revises: e7671ba0428a
Create Date: 2024-11-18 20:50:23.358367+03:00

"""

from typing import (
    Sequence,
    Union,
)

import sqlalchemy as sa
from alembic import op

revision: str = "b58757c14d8d"
down_revision: Union[str, None] = "e7671ba0428a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "request_cache",
        sa.Column("hash", sa.String(length=256), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hash"),
        comment="Кешированные данные запроса",
    )


def downgrade() -> None:
    op.drop_table("request_cache")
