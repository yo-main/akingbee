"""initial migration

Revision ID: 2ddfd99e0bb4
Revises:
Create Date: 2021-01-25 22:42:56.598121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2ddfd99e0bb4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.TEXT(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_table(
        "credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.TEXT(), nullable=False),
        sa.Column("password", postgresql.BYTEA(), nullable=False),
        sa.Column("last_seen", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_credentials_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_credentials")),
        sa.UniqueConstraint("username", name=op.f("uq_credentials_username")),
    )
    op.create_table(
        "event_statuses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_event_statuses_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event_statuses")),
    )
    op.create_table(
        "event_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_event_types_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event_types")),
    )
    op.create_table(
        "hive_conditions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_hive_conditions_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_hive_conditions")),
    )
    op.create_table(
        "honey_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_honey_types_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_honey_types")),
    )
    op.create_table(
        "owners",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_owners_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_owners")),
    )
    op.create_table(
        "swarm_health_statuses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_swarm_health_statuses_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_swarm_health_statuses")),
    )
    op.create_table(
        "apiaries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("location", sa.TEXT(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("honey_type_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["honey_type_id"],
            ["honey_types.id"],
            name=op.f("fk_apiaries_honey_type_id_honey_types"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_apiaries_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_apiaries")),
    )
    op.create_table(
        "swarms",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("health_status_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["health_status_id"],
            ["swarm_health_statuses.id"],
            name=op.f("fk_swarms_health_status_id_swarm_health_statuses"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_swarms_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_swarms")),
    )
    op.create_table(
        "hives",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("condition_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("swarm_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("apiary_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["apiary_id"], ["apiaries.id"], name=op.f("fk_hives_apiary_id_apiaries")
        ),
        sa.ForeignKeyConstraint(
            ["condition_id"],
            ["hive_conditions.id"],
            name=op.f("fk_hives_condition_id_hive_conditions"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["owners.id"], name=op.f("fk_hives_owner_id_owners")
        ),
        sa.ForeignKeyConstraint(
            ["swarm_id"], ["swarms.id"], name=op.f("fk_hives_swarm_id_swarms")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_hives_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_hives")),
    )
    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("due_date", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("type_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hive_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["hive_id"], ["hives.id"], name=op.f("fk_events_hive_id_hives")
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["event_statuses.id"],
            name=op.f("fk_events_status_id_event_statuses"),
        ),
        sa.ForeignKeyConstraint(
            ["type_id"], ["event_types.id"], name=op.f("fk_events_type_id_event_types")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_events_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_events")),
    )
    op.create_table(
        "comments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("comment", sa.TEXT(), nullable=False),
        sa.Column("type", sa.TEXT(), nullable=False),
        sa.Column("date", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("swarm_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("hive_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_id"], ["events.id"], name=op.f("fk_comments_event_id_events")
        ),
        sa.ForeignKeyConstraint(
            ["hive_id"], ["hives.id"], name=op.f("fk_comments_hive_id_hives")
        ),
        sa.ForeignKeyConstraint(
            ["swarm_id"], ["swarms.id"], name=op.f("fk_comments_swarm_id_swarms")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_comments_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comments")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comments")
    op.drop_table("events")
    op.drop_table("hives")
    op.drop_table("swarms")
    op.drop_table("apiaries")
    op.drop_table("swarm_health_statuses")
    op.drop_table("owners")
    op.drop_table("honey_types")
    op.drop_table("hive_conditions")
    op.drop_table("event_types")
    op.drop_table("event_statuses")
    op.drop_table("credentials")
    op.drop_table("users")
    op.drop_table("comment_types")
    # ### end Alembic commands ###
