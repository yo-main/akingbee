from src.models import MODELS
from src.database import DB


with DB:
    DB.drop_tables(MODELS)
