from src.data_access import pw_objects as obj
from src.data_access.connectors import DB
from src.data_access.pw_objects import CommentType, StatusAction

with DB:
    DB.create_tables(obj.MODELS)
    

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
 