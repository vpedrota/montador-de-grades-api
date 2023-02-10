from flask import Flask, request
from service.modeling import Modeling
from flask_cors import CORS
from flask_cors import cross_origin
import os

app = Flask(__name__)
ucs = Modeling()
CORS(app)

class Grade():

    @app.route("/disciplinas", methods=['GET'])
    @cross_origin()
    def get():
        return ucs.get_ucs()

    @app.route("/disciplinas", methods=['POST'])
    @cross_origin()
    def post_uc():
        data = request.get_json()
        return ucs.uc_analizer(data['items'])

    @app.route("/prof", methods=['POST'])
    @cross_origin()
    def post_prof():
        data = request.get_json()
        return ucs.prof_analizer(data['items'])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))