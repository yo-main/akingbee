import flask

from src.constants import FRENCH, ENGLISH
from src.log.logger import logger


class BaseSuccess:
    fr = "Non traduit"
    en = "Not translated"

    def __new__(self, log=True):

        if log:
            logger.info(self.en)

        return flask.jsonify(
            {"status": "success", FRENCH: self.fr, ENGLISH: self.en}
        )
