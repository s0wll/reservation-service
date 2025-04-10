"""add tables and reservations tables

Revision ID: 21dfe41539f8
Revises:
Create Date: 2025-04-10 12:16:35.728555

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "21dfe41539f8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tables",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("seats", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_name", sa.String(length=100), nullable=False),
        sa.Column("table_id", sa.Integer(), nullable=False),
        sa.Column("reservation_time", sa.DateTime(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["tables.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("reservations")
    op.drop_table("tables")
