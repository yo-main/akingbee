"""change owner_id to owner

Revision ID: efd4c6888637
Revises: 4ff9a4c23805
Create Date: 2023-01-24 22:21:42.339520

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "efd4c6888637"
down_revision = "4ff9a4c23805"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("hive", sa.Column("owner", sa.String(), nullable=False))
    op.drop_column("hive", "owner_id")
    op.create_unique_constraint(None, "parameter", ["key", "value", "organization_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "parameter", type_="unique")
    op.add_column("hive", sa.Column("owner_id", sa.UUID(), autoincrement=False, nullable=False))
    op.drop_column("hive", "owner")
    # ### end Alembic commands ###
