import sys
import os
from yaml import load, Loader


PROJECT_PATH = os.getcwd()

PLATFORM_ENVIRONMENT = os.environ.get("AKB_ENVIRONMENT") or "TEST"
assert PLATFORM_ENVIRONMENT in ("TEST", "PROD", "SIMU")

# PATHS
FLASK_URL_ROOT = ""
FLASK_URL_SESSION = os.path.join(PROJECT_PATH, "flask_session")
IMAGES_FOLDER = os.path.join(PROJECT_PATH, "images")
LOG_DIRECTORY = os.path.join(PROJECT_PATH, "log")
ACTIVITY_LOG = "activity.log"

# create missing folders
if not os.path.exists(LOG_DIRECTORY):
    os.mkdir(LOG_DIRECTORY)
if not os.path.exists(FLASK_URL_SESSION):
    os.mkdir(FLASK_URL_SESSION)


FLASK_SECRET_KEY = os.environ.get("AKB_SECRET_KEY")


# DATABASE
DATABASE = {
    "SIMU": {
        "user": os.environ.get("AKB_TEST_DB_USER"),
        "password": os.environ.get("AKB_TEST_DB_PASSWORD"),
        "host": os.environ.get("AKB_TEST_DB_HOST"),
        "database": os.environ.get("AKB_TEST_DB_DATABASE"),
    },
    "PROD": {
        "user": os.environ.get("AKB_PROD_DB_USER"),
        "password": os.environ.get("AKB_PROD_DB_PASSWORD"),
        "host": os.environ.get("AKB_PROD_DB_HOST"),
        "database": os.environ.get("AKB_PROD_DB_DATABASE"),
    },
}

USER_ID = None
PASSWORD_REQUESTED = True
