"""Prepopulating dependent tables

Revision ID: ab2d8af67f1f
Revises: 6af38957fbda
Create Date: 2026-02-09 22:28:00.946351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ab2d8af67f1f'
down_revision: Union[str, Sequence[str], None] = '6af38957fbda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    member_roles_table = sa.table(
        "MemberRole",
        sa.column("role", sa.String),
    )

    op.bulk_insert(
        member_roles_table,
        [
            {"role": "admin"},
            {"role": "coach"},
            {"role": "officer"},
            {"role": "member"},
            {"role": "inactive"},
        ],
    )

    semester_table = sa.table(
        "Semester",
        sa.column("semester", sa.String),
    )

    op.bulk_insert(
        semester_table,
        [
            {"semester":"spring"},
            {"semester":"summer"},
            {"semester":"fall"},
        ]
    )




def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "TRUNCATE TABLE MemberRole CASCADE;"
    )