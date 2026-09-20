"""Add generated timestamp default

Revision ID: 859aada37902
Revises: 5191dd43362f
Create Date: 2026-09-20 02:25:11.971561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '859aada37902'
down_revision: Union[str, None] = '5191dd43362f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "personal_data",
        "ts_gen",
        server_default=sa.text("now()"),
    )

    op.alter_column(
        "residences",
        "ts_gen",
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "residences",
        "ts_gen",
        server_default=None,
    )

    op.alter_column(
        "personal_data",
        "ts_gen",
        server_default=None,
    )   
