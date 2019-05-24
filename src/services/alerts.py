import flask
import werkzeug

from src.constants.config import FRENCH, ENGLISH
from src.locals import alerts_fr as fr
from src.locals import alerts_en as en
from app import app


class Error(Exception):
    def __init__(self, code):
        super().__init__(self)
        self.code = code

        self.out = {}
        self.out['status'] = "error"
        self.out['code'] = code

        self._generate_msg()

    def _generate_msg(self):
        self.out[FRENCH], self.out[ENGLISH] = {}, {}
        self.out[FRENCH]['message'] = fr.errors[self.code]
        self.out[FRENCH]['title'] = "Erreur # {:05d}".format(self.code)
        self.out[ENGLISH]['message'] = en.errors[self.code]
        self.out[ENGLISH]['title'] = "Error # {:05d}".format(self.code)

    def to_dict(self):
        return self.out


@app.errorhandler(Error)
def handle_error(error):
    response = flask.jsonify(error.to_dict())
    return response, 500




def Success(code=None):
    out = {
        'status': "success",
        'code': code,
    }

    if code:
        out[FRENCH], out[ENGLISH] = {}, {}
        out[FRENCH]['title'], out[FRENCH]['message'] = fr.successes[code]
        out[ENGLISH]['title'], out[ENGLISH]['message'] = en.successes[code]

    return flask.jsonify(out)

