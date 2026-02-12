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

    role_permissions_table = sa.table(
        "RolePermissions",
        sa.column("role", sa.String),
        sa.column("access_site", sa.Boolean),
        sa.column("create_announcements", sa.Boolean),
        sa.column("manage_dates", sa.Boolean),
        sa.column("manage_members", sa.Boolean),
        sa.column("manage_roles", sa.Boolean),
        sa.column("view_funds", sa.Boolean),
        sa.column("view_roster", sa.Boolean),
    )

    op.bulk_insert(
        role_permissions_table,
        [
            {"role":"admin", "access_site":True,"create_announcements":True,"manage_dates":True,"manage_members":True,"manage_roles":True,"view_funds":True,"view_roster":True},
            {"role":"coach", "access_site":True,"create_announcements":True,"manage_dates":True,"manage_members":False,"manage_roles":False,"view_funds":True,"view_roster":True},
            {"role":"officer", "access_site":True,"create_announcements":True,"manage_dates":True,"manage_members":True,"manage_roles":True,"view_funds":True,"view_roster":True},
            {"role":"member", "access_site":True,"create_announcements":False,"manage_dates":False,"manage_members":False,"manage_roles":False,"view_funds":False,"view_roster":True},
            {"role":"inactive", "access_site":False,"create_announcements":False,"manage_dates":False,"manage_members":False,"manage_roles":False,"view_funds":False,"view_roster":True},
        ]
    )




def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        'TRUNCATE TABLE "MemberRole" CASCADE;'
    )

    op.execute(
        'TRUNCATE TABLE "RolePermissions";'
    )