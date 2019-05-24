import os
from yaml import load, Loader

with open("environment.yaml", "r") as stream:
    ENV = load(stream, Loader=Loader)


ROOT_PATH = ENV['project_path']

PLATFORM_ENVIRONMENT = ENV['platform']
assert PLATFORM_ENVIRONMENT in ('TEST', 'PROD')

URL_ROOT = ENV['url_root']
URL_FLASK_SESSION = os.path.join(URL_ROOT, 'flask_session')


