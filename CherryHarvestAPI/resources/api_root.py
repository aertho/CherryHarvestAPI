from CherryHarvestAPI import app
from flask import url_for
from flask.ext.restful import Resource


class APIRoot(Resource):
    def get(self):
        return {
            "lugs" : url_for('lugs', _external=True, _scheme=app.config["SCHEME"]),
            "pickers" : url_for('pickers', _external=True, _scheme=app.config["SCHEME"]),
            "blocks" : url_for('blocks', _external=True, _scheme=app.config["SCHEME"]),
            "orchard_loads" : url_for('orchard_loads', _external=True, _scheme=app.config["SCHEME"]),
            "farm_loads" : url_for('farm_loads', _external=True, _scheme=app.config["SCHEME"]),
        }