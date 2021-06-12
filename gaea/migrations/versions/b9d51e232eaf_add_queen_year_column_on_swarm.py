"""add queen year column on swarm

Revision ID: b9d51e232eaf
Revises: 0ac840331a60
Create Date: 2021-06-12 15:55:01.976628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b9d51e232eaf"
down_revision = "0ac840331a60"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("swarms", sa.Column("queen_year", sa.INTEGER(), nullable=True))
    op.execute("UPDATE swarms SET queen_year = 1900 WHERE queen_year IS NULL")
    op.alter_column("swarms", "queen_year", nullable=False)


def downgrade():
    op.drop_column("swarms", "queen_year")
