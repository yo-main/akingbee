from src.models import MODELS, CommentType, StatusAction
from src.database import DB

with DB:
    DB.create_tables(MODELS)
    

COMMENT_TYPES = (
    {"fr": "Utilisateur", "en": "User"},
    {"fr": "Système", "en": "System"},
    {"fr": "Action", "en": "Action"},
)

ACTION_STATUS = (
    {"fr": "Fait", "en": "Done"},
    {"fr": "En attente", "en": "Pending"},
)

with DB:
    for data in COMMENT_TYPES:
        entry = CommentType(**data)
        entry.save()
        
    for data in ACTION_STATUS:
        entry = StatusAction(**data)
        entry.save()
 