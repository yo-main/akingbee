"""add triggers

Revision ID: 8d9f03d62087
Revises: 696284ff5e09
Create Date: 2020-11-08 11:23:38.220272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d9f03d62087'
down_revision = '2ddfd99e0bb4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE FUNCTION check_user_swarms() RETURNS trigger AS $check_user_swarms$
            BEGIN
                IF NEW.user_id NOT IN (SELECT t.user_id FROM swarm_health_statuses as t WHERE t.id = NEW.health_status_id) THEN
                    RAISE EXCEPTION 'Different user for swarm_health_statuses';
                END IF;

                RETURN NEW;
            END;
        $check_user_swarms$ LANGUAGE plpgsql;
        CREATE TRIGGER trigger_user_swarms BEFORE INSERT OR UPDATE ON swarms
            FOR EACH ROW EXECUTE PROCEDURE check_user_swarms();

    """)

    op.execute("""
        CREATE FUNCTION check_user_apiaries() RETURNS trigger AS $check_user_apiaries$
            BEGIN
                IF NEW.user_id NOT IN (SELECT t.user_id FROM honey_types as t WHERE t.id = NEW.honey_type_id) THEN
                    RAISE EXCEPTION 'Different user for honey_type';
                END IF;

                RETURN NEW;
            END;
        $check_user_apiaries$ LANGUAGE plpgsql;
        CREATE TRIGGER trigger_user_apiaries BEFORE INSERT OR UPDATE ON apiaries
            FOR EACH ROW EXECUTE PROCEDURE check_user_apiaries();
    """)

    op.execute("""
        CREATE FUNCTION check_user_hives() RETURNS trigger AS $check_user_hives$
            BEGIN
                IF NEW.user_id NOT IN (SELECT s.user_id FROM owners as s WHERE s.id = NEW.owner_id) THEN
                    RAISE EXCEPTION 'Different user for owners';
                END IF;

                IF NEW.swarm_id IS NOT NULL AND NEW.user_id NOT IN (SELECT s.user_id FROM swarms as s WHERE s.id = NEW.swarm_id) THEN
                    RAISE EXCEPTION 'Different user for swarms';
                END IF;

                IF NEW.apiary_id IS NOT NULL AND NEW.user_id NOT IN (SELECT s.user_id FROM apiaries as s WHERE s.id = NEW.apiary_id) THEN
                    RAISE EXCEPTION 'Different user for apiaries';
                END IF;

                IF NEW.user_id NOT IN (SELECT s.user_id FROM hive_conditions as s WHERE s.id = NEW.condition_id) THEN
                    RAISE EXCEPTION 'Different user for hive_conditions';
                END IF;

                RETURN NEW;
            END;
        $check_user_hives$ LANGUAGE PLPGSQL;
        CREATE TRIGGER trigger_user_hives BEFORE INSERT OR UPDATE ON hives
            FOR EACH ROW EXECUTE PROCEDURE check_user_hives();
    """)

    op.execute("""
        CREATE FUNCTION check_user_events() RETURNS trigger AS $check_user_events$
            BEGIN
                IF NEW.user_id NOT IN (SELECT t.user_id FROM event_types as t WHERE t.id = NEW.type_id) THEN
                    RAISE EXCEPTION 'Different user for event_types';
                END IF;

                IF NEW.user_id NOT IN (SELECT t.user_id FROM event_statuses as t WHERE t.id = NEW.status_id) THEN
                    RAISE EXCEPTION 'Different user for event_statuses';
                END IF;

                IF NEW.hive_id IS NOT NULL AND NEW.user_id NOT IN (SELECT t.user_id FROM hives as t WHERE t.id = NEW.hive_id) THEN
                    RAISE EXCEPTION 'Different user for hives';
                END IF;

                RETURN NEW;
            END;
        $check_user_events$ LANGUAGE PLPGSQL;
        CREATE TRIGGER trigger_user_events BEFORE INSERT OR UPDATE ON events
            FOR EACH ROW EXECUTE PROCEDURE check_user_events();
    """)

    op.execute("""
        CREATE FUNCTION check_user_comments() RETURNS trigger AS $check_user_comments$
            BEGIN
                IF new.event_id IS NOT NULL AND NEW.user_id NOT IN (SELECT t.user_id FROM events as t WHERE t.id = NEW.event_id) THEN
                    RAISE EXCEPTION 'Different user for eventd';
                END IF;

                IF NEW.swarm_id IS NOT NULL AND NEW.user_id NOT IN (SELECT t.user_id FROM swarms as t WHERE t.id = NEW.swarm_id) THEN
                    RAISE EXCEPTION 'Different user for swarms';
                END IF;

                IF NEW.hive_id IS NOT NULL AND NEW.user_id NOT IN (SELECT t.user_id FROM hives as t WHERE t.id = NEW.hive_id) THEN
                    RAISE EXCEPTION 'Different user for hives';
                END IF;

                RETURN NEW;
            END;
        $check_user_comments$ LANGUAGE PLPGSQL;
        CREATE TRIGGER trigger_user_comments BEFORE INSERT OR UPDATE ON comments
            FOR EACH ROW EXECUTE PROCEDURE check_user_comments();
    """)

def downgrade():
    op.execute("DROP TRIGGER trigger_user_swarms ON swarms")
    op.execute("DROP FUNCTION check_user_swarms")
    op.execute("DROP TRIGGER trigger_user_hives ON hives")
    op.execute("DROP FUNCTION check_user_hives")
    op.execute("DROP TRIGGER trigger_user_apiaries ON apiaries")
    op.execute("DROP FUNCTION check_user_apiaries")
    op.execute("DROP TRIGGER trigger_user_events ON events")
    op.execute("DROP FUNCTION check_user_events")
    op.execute("DROP TRIGGER trigger_user_comments ON comments")
    op.execute("DROP FUNCTION check_user_comments")