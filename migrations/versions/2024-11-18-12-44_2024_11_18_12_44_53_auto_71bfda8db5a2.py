"""2024-11-18_12-44-53-auto

Revision ID: 71bfda8db5a2
Revises: e7671ba0428a
Create Date: 2024-11-18 12:44:53.716279+03:00
"""

from typing import (
    Sequence,
    Union,
)

import sqlalchemy as sa
from alembic import op

revision: str = "71bfda8db5a2"
down_revision: Union[str, None] = "e7671ba0428a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "coordinate_reference_system",
        sa.Column("srid", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        comment="Система координат",
    )


def downgrade() -> None:
    op.drop_table("coordinate_reference_system")
