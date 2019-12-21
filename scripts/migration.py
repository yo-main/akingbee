from src.models import MODELS, CommentType, StatusEvent
from src.database import DB

with DB:
    DB.create_tables(MODELS)


COMMENT_TYPES = (
    {"fr": "Utilisateur", "en": "User"},
    {"fr": "Système", "en": "System"},
    {"fr": "Évènement", "en": "Event"},
)

EVENT_STATUS = (
    {"fr": "Fait", "en": "Done"},
    {"fr": "En attente", "en": "Pending"},
)

with DB:
    for data in COMMENT_TYPES:
        entry = CommentType(**data)
        entry.save()

    for data in EVENT_STATUS:
        entry = StatusEvent(**data)
        entry.save()

