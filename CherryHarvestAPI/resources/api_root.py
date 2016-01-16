from CherryHarvestAPI import app
from flask import url_for
from flask.ext.restful import Resource


class APIRoot(Resource):
    def get(self):
        return {
            "lugs" : url_for('lugs', _external=True, _scheme=app.config["SCHEME"]),
            "lug_pickers" : url_for('lug_pickers', _external=True, _scheme=app.config["SCHEME"]),
            "pickers" : url_for('pickers', _external=True, _scheme=app.config["SCHEME"]),
            "blocks" : url_for('blocks', _external=True, _scheme=app.config["SCHEME"]),
            "orchard_loads" : url_for('orchard_loads', _external=True, _scheme=app.config["SCHEME"]),
            "farm_loads" : url_for('farm_loads', _external=True, _scheme=app.config["SCHEME"]),
            "picker_numbers" : url_for('picker_numbers', _external=True, _scheme=app.config["SCHEME"]),
            "tags" : url_for('tags', _external=True, _scheme=app.config["SCHEME"]),
            "days" : url_for('days', _external=True, _scheme=app.config["SCHEME"]),
            "seasons" : url_for('seasons', _external=True, _scheme=app.config["SCHEME"])
        }