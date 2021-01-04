from .views.apiaries import router as router_apiary
from .views.hives import router as router_hive
from .views.setup import router as router_setup
from .views.swarms import router as router_swarm

ROUTERS = (router_apiary, router_hive, router_setup, router_swarm)