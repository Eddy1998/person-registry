"""Add exclusion constraints for valid periods

Revision ID: 5191dd43362f
Revises: d82165792acd
Create Date: 2026-09-20 02:07:28.618376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5191dd43362f'
down_revision: Union[str, None] = 'd82165792acd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.execute(
        """
        ALTER TABLE personal_data
        ADD CONSTRAINT ex_personal_data_no_overlap
        EXCLUDE USING gist (
            person_id WITH =,
            daterange(valid_from, valid_to, '[]') WITH &&
        )
        """
    )

    op.execute(
        """
        ALTER TABLE residences
        ADD CONSTRAINT ex_residences_no_overlap
        EXCLUDE USING gist (
            person_id WITH =,
            daterange(valid_from, valid_to, '[]') WITH &&
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE residences
        DROP CONSTRAINT ex_residences_no_overlap
        """
    )

    op.execute(
        """
        ALTER TABLE personal_data
        DROP CONSTRAINT ex_personal_data_no_overlap
        """
    )

    op.execute("DROP EXTENSION IF EXISTS btree_gist")