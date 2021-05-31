from .views.apiaries import router as router_apiary
from .views.hives import router as router_hive
from .views.setup import router as router_setup
from .views.swarms import router as router_swarm
from .views.comments import router as router_comments
from .views.events import router as router_events

ROUTERS = (
    router_apiary,
    router_hive,
    router_setup,
    router_swarm,
    router_comments,
    router_events,
)
