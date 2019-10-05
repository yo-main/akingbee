import sys
import os
import peewee as pw
from yaml import load, Loader


CONFIG_FILE_NAME = "environment.yaml"
if os.path.exists(CONFIG_FILE_NAME):
    CONFIG_FILE_PATH = CONFIG_FILE_NAME
else:
    CONFIG_FILE_PATH = os.path.join(sys.path[0], "environment.yaml")

with open(CONFIG_FILE_PATH, "r") as stream:
    ENV = load(stream, Loader=Loader)

PROJECT_PATH = os.getcwd()

PLATFORM_ENVIRONMENT = ENV["platform"]
assert PLATFORM_ENVIRONMENT in ("TEST", "PROD")

# PATHS
FLASK_URL_ROOT = ENV["url_root"]
FLASK_URL_SESSION = os.path.join(PROJECT_PATH, "flask_session")
IMAGES_FOLDER = os.path.join(PROJECT_PATH, "images")
LOG_DIRECTORY = os.path.join(PROJECT_PATH, "log")
ACTIVITY_LOG = "activity.log"

# environment variables
FLASK_SECRET_KEY = os.environ.get("AKB_SECRET_KEY")


# DATABASE
DATABASE = {
    "TEST": {
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
PASSWORD_REQUESTED = ENV["password_requested"]
