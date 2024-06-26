"""test

Revision ID: 95891afca307
Revises: 9a9309eb386b
Create Date: 2023-05-21 15:58:09.563237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95891afca307"
down_revision = "9a9309eb386b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("comment_event_id_fkey", "comment", type_="foreignkey")
    op.drop_constraint("comment_hive_id_fkey", "comment", type_="foreignkey")
    op.create_foreign_key(None, "comment", "hive", ["hive_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key(None, "comment", "event", ["event_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "comment", type_="foreignkey")
    op.drop_constraint(None, "comment", type_="foreignkey")
    op.create_foreign_key("comment_hive_id_fkey", "comment", "hive", ["hive_id"], ["id"])
    op.create_foreign_key("comment_event_id_fkey", "comment", "event", ["event_id"], ["id"])
    # ### end Alembic commands ###
