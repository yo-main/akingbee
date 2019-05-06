import flask

from src.constants.config import FRENCH, ENGLISH
from src.locals import alerts_fr as fr
from src.locals import alerts_en as en


class Error(Exception):
    def __init__(self, code):
        self.result = "error"
        self.code = code
        self.message = {}

        self._generate_msg()

    def _generate_msg(self):
        self.message[FRENCH] = fr.errors[self.code]
        self.message[ENGLISH] = en.errors[self.code]


def Success(code=None):
    out = {
        'result': "success",
        'code': code,
        'title': "",
        'message': ""
    }

    if code:
        if flask.session['language'] == FRENCH:
            out['title'], out['message'] = fr.successes[code]
        else:
            out['title'], out['message'] = en.successes[code]

    return flask.jsonify(out)

