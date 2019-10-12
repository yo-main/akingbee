import datetime
import functools

from src.models import Comment, Swarm


def update_swarm_health(swarm_id):
    if swarm_id is None:
        return False

    comments = list(
        Comment.select()
        .where(Comment.swarm == swarm_id)
        .order_by(Comment.date.desc())
    )

    if comments:
        swarm = Swarm.get_by_id(swarm_id)
        swarm.health = comments[0].health
        swarm.save()

    return True



