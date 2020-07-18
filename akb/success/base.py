import flask

from common.log.logger import logger

from akb.constants import FRENCH, ENGLISH


class BaseSuccess:
    fr = "Non traduit"
    en = "Not translated"

    def __new__(self, log=True):

        if log:
            logger.info(self.en)

        return flask.jsonify(
            {"status": "success", FRENCH: self.fr, ENGLISH: self.en}
        )
