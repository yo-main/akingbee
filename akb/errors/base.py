import json

import flask

from akb.constants import FRENCH, ENGLISH

from common.log.logger import logger


class BaseError(Exception):
    code = 400
    reference = 0
    fr = "Non traduit"
    en = "Not translated"

    def __init__(self, log=True, **kwargs):
        if log:
            kwargs["code"] = self.code
            kwargs["description"] = self.en
            logger.error(kwargs)

    def to_dict(self):
        return flask.jsonify(
            {
                "code": self.code,
                FRENCH: {
                    "title": f"Erreur {self.reference:05d}",
                    "message": self.fr,
                },
                ENGLISH: {
                    "title": f"Error {self.reference:05d}",
                    "message": self.en,
                },
            }
        )
