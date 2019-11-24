import flask
import werkzeug

from src.constants.config import FRENCH, ENGLISH
from src.locals import alerts_fr as fr
from src.locals import alerts_en as en
from src.services.logger import logger


class Error(Exception):
    def __init__(self, code):
        super().__init__(self)
        self.code = code

        self.out = {}
        self.out["status"] = "error"
        self.out["code"] = code

        self._generate_msg()

        if ENGLISH in self.out:
            logger.error(self.out[ENGLISH])

    def _generate_msg(self):
        self.out[FRENCH], self.out[ENGLISH] = {}, {}
        self.out[FRENCH]["message"] = fr.errors[self.code]
        self.out[FRENCH]["title"] = "Erreur # {:05d}".format(self.code)
        self.out[ENGLISH]["message"] = en.errors[self.code]
        self.out[ENGLISH]["title"] = "Error # {:05d}".format(self.code)

    def to_dict(self):
        return self.out


def Success(code=None):
    out = {"status": "success", "code": code}

    if code:
        out[FRENCH], out[ENGLISH] = {}, {}
        out[FRENCH]["title"], out[FRENCH]["message"] = fr.successes[code]
        out[ENGLISH]["title"], out[ENGLISH]["message"] = en.successes[code]

    if ENGLISH in out:
        logger.info(out[ENGLISH])

    return flask.jsonify(out)
