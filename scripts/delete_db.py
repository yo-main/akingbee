from src.data_access import pw_objects as obj
from src.data_access.connectors import DB


with DB:
    DB.drop_tables(obj.MODELS)
