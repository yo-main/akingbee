import sys
import os
from dataclasses import dataclass
from yaml import load, Loader


class Config:
    LOGS_FOLDER_NAME = "log"
    LOGS_FILE_NAME = "akb.log"
    IMAGES_FOLDER_NAME = "images"
    FLASK_SESSIONS_FOLDER_NAME = "flask_session"

    PATH_PROJECT = os.getcwd()
    PATH_LOGS = os.path.join(PATH_PROJECT, LOGS_FOLDER_NAME)
    PATH_IMAGES = os.path.join(PATH_PROJECT, IMAGES_FOLDER_NAME)
    PATH_FLASK_SESSIONS = os.path.join(
        PATH_PROJECT, FLASK_SESSIONS_FOLDER_NAME
    )

    URL_PREFIX = ""

    ENV = os.environ.get("ENV", "SIMU")
    SECRET_KEY = "DEV"
    PASSWORD_REQUESTED = True

    FLASK_DEBUG = False

    DATABASE = {}
    DATABASE_HOST = None
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_SIMU = "akb_test"
    DATABASE_PROD = "akb"

    def __init__(self):
        self.load_env_file()
        self.validate()
        self.create_missing_folders()
        self.load_database_conf()

    def validate(self):
        assert self.ENV in ("TEST", "PROD", "SIMU")

    def load_env_file(self):
        if os.path.exists(".env"):
            for row in open(".env"):
                row = row.strip()  # get rid of empty lines
                if row:
                    var_name, var_value = row.split("=")

                    if var_name in os.environ:
                        var_value = os.environ[var_name]

                    if var_value == "true":
                        var_value = True
                    elif var_value == "false":
                        var_value = False

                    setattr(self, var_name, var_value)

    def create_missing_folders(self):
        paths = (self.PATH_LOGS, self.PATH_FLASK_SESSIONS)

        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def load_database_conf(self):
        if self.ENV not in ("SIMU", "PROD"):
            return

        self.DATABASE = {
            "host": self.DATABASE_HOST,
            "user": self.DATABASE_USER,
            "password": self.DATABASE_PASSWORD,
            "database": getattr(self, f"DATABASE_{self.ENV}"),
        }
