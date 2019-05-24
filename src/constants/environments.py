import os
from yaml import load, Loader

with open("environment.yaml", "r") as stream:
    ENV = load(stream, Loader=Loader)


PROJECT_PATH = ENV['project_path']

PLATFORM_ENVIRONMENT = ENV['platform']
assert PLATFORM_ENVIRONMENT in ('TEST', 'PROD')

URL_ROOT = ENV['url_root']
URL_FLASK_SESSION = os.path.join(PROJECT_PATH, 'flask_session')

LOG_DIRECTORY = os.path.join(PROJECT_PATH, 'logs.log')
