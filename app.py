from flask import Flask, request
from service.modeling import Modeling
from flask_cors import CORS
import os

app = Flask(__name__)


CORS(app, origins=['https://montador-de-grades-upfpc35ezq-uc.a.run.app'])

ucs = Modeling()

class Grade():

    @app.route("/disciplinas", methods=['GET'])
    def get():
        return ucs.get_ucs()

    @app.route("/disciplinas", methods=['POST'])
    def post_uc():
        data = request.get_json()
        return ucs.uc_analizer(data['items'])

    @app.route("/disciplinas/prof", methods=['POST'])
    def post_prof():
        data = request.get_json()
        return ucs.prof_analizer(data['items'])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
