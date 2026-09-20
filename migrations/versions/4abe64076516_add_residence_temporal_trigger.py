"""Add residence temporal trigger

Revision ID: 4abe64076516
Revises: 2e2f80b672b8
Create Date: 2026-09-20 02:59:19.592304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4abe64076516'
down_revision: Union[str, None] = '2e2f80b672b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION manage_residence_temporal()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        DECLARE
            previous_snapshot residences%ROWTYPE;
            next_snapshot residences%ROWTYPE;
        BEGIN
            SELECT *
            INTO previous_snapshot
            FROM residences
            WHERE person_id = NEW.person_id
              AND valid_from < NEW.valid_from
            ORDER BY valid_from DESC
            LIMIT 1
            FOR UPDATE;

            SELECT *
            INTO next_snapshot
            FROM residences
            WHERE person_id = NEW.person_id
              AND valid_from > NEW.valid_from
            ORDER BY valid_from ASC
            LIMIT 1;

            IF previous_snapshot.id IS NOT NULL THEN
                UPDATE residences
                SET valid_to = NEW.valid_from - 1,
                    ts_update = now()
                WHERE id = previous_snapshot.id;
            END IF;

            IF next_snapshot.id IS NOT NULL THEN
                NEW.valid_to := next_snapshot.valid_from - 1;
            ELSE
                NEW.valid_to := DATE '9999-12-31';
            END IF;

            RETURN NEW;
        END;
        $$;
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_manage_residence_temporal
        BEFORE INSERT ON residences
        FOR EACH ROW
        EXECUTE FUNCTION manage_residence_temporal();
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS trg_manage_residence_temporal
        ON residences;
        """
    )

    op.execute(
        """
        DROP FUNCTION IF EXISTS manage_residence_temporal();
        """
    )