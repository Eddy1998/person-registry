"""add personal data trigger

Revision ID: 2e2f80b672b8
Revises: 859aada37902
Create Date: 2026-09-20 02:38:55.762754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e2f80b672b8'
down_revision: Union[str, None] = '859aada37902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION manage_personal_data_temporal()
        RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        DECLARE
            previous_snapshot personal_data%ROWTYPE;
            next_snapshot personal_data%ROWTYPE;
        BEGIN
            SELECT *
            INTO previous_snapshot
            FROM personal_data
            WHERE person_id = NEW.person_id
              AND valid_from < NEW.valid_from
            ORDER BY valid_from DESC
            LIMIT 1
            FOR UPDATE;

            SELECT *
            INTO next_snapshot
            FROM personal_data
            WHERE person_id = NEW.person_id
              AND valid_from > NEW.valid_from
            ORDER BY valid_from ASC
            LIMIT 1;

            IF previous_snapshot.id IS NOT NULL THEN
                UPDATE personal_data
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
        CREATE TRIGGER trg_manage_personal_data_temporal
        BEFORE INSERT ON personal_data
        FOR EACH ROW
        EXECUTE FUNCTION manage_personal_data_temporal();
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS trg_manage_personal_data_temporal
        ON personal_data;
        """
    )

    op.execute(
        """
        DROP FUNCTION IF EXISTS manage_personal_data_temporal();
        """
    )
