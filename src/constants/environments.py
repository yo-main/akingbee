import sys
import os
from yaml import load, Loader


CONFIG_FILE_NAME = "environment.yaml"

# I don't remember the reason of below's funny thing but doesn't seem to be a problem anymore
# Leaving this comment here just in case it might create some issue I don't see yet in the future
#if os.path.exists(CONFIG_FILE_NAME):
#    CONFIG_FILE_PATH = CONFIG_FILE_NAME
#else:
#     CONFIG_FILE_PATH = os.path.join(sys.path[0], "environment.yaml")


PROJECT_PATH = os.getcwd()

PLATFORM_ENVIRONMENT = os.environ.get("AKB_ENVIRONMENT") or "DEV"
assert PLATFORM_ENVIRONMENT in ("SIMU", "PROD", "DEV")

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
    }
}

USER_ID = None
PASSWORD_REQUESTED = True
