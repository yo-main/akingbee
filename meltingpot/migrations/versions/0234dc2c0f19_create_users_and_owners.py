"""create users and owners

Revision ID: 0234dc2c0f19
Revises:
Create Date: 2020-08-09 23:46:14.725328

"""
from alembic import op
import sqlalchemy as sa
import meltingpot
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "0234dc2c0f19"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "owners",
        sa.Column("id", meltingpot.models.base.UUID(length=16), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=256), nullable=True),
        sa.Column("date_creation", mysql.DATETIME(), nullable=True),
        sa.Column("date_modification", mysql.DATETIME(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_owners")),
        sa.UniqueConstraint("id", name=op.f("uq_owners_id")),
    )
    op.create_table(
        "users",
        sa.Column("id", meltingpot.models.base.UUID(length=16), nullable=False),
        sa.Column("username", mysql.VARCHAR(length=256), nullable=True),
        sa.Column("pwd", mysql.VARCHAR(length=256), nullable=True),
        sa.Column("email", mysql.VARCHAR(length=256), nullable=True),
        sa.Column("created_at", mysql.DATETIME(), nullable=True),
        sa.Column("updated_at", mysql.DATETIME(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("id", name=op.f("uq_users_id")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_table("owners")
    # ### end Alembic commands ###
