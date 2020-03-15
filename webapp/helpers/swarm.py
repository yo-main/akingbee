import datetime
import functools

from common.models import Comment, Swarm


def update_swarm_health(hive_id, swarm_id):
    if swarm_id is None:
        return False

    comments = list(
        Comment.select(Comment)
        .where(Comment.swarm == swarm_id, Comment.health.is_null(False))
        .order_by(Comment.date.desc())
    )

    if comments:
        swarm = Swarm.get_by_id(swarm_id)
        swarm.health = comments[0].health
        swarm.save()

    return True
