import sys
import os
from yaml import load, Loader


CONFIG_FILE_PATH = os.path.join(sys.path[0], "environment.yaml")

with open(CONFIG_FILE_PATH, "r") as stream:
    ENV = load(stream, Loader=Loader)


PROJECT_PATH = ENV['project_path']

PLATFORM_ENVIRONMENT = ENV['platform']
assert PLATFORM_ENVIRONMENT in ('TEST', 'PROD')

URL_ROOT = ENV['url_root']
URL_FLASK_SESSION = os.path.join(PROJECT_PATH, 'flask_session')

LOG_DIRECTORY = os.path.join(PROJECT_PATH, 'logs.log')

USER_ID = None
