from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI import models, app
from CherryHarvestAPI.resources.common import NestedWithEmpty
from CherryHarvestAPI.resources.picker import picker_fields
from flask import jsonify, request
from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

lug_picker_fields = {
    'contribution' : fields.Float,
    'picker_id' : fields.Integer,
    'picker' : NestedWithEmpty({'href' : fields.Url('picker', absolute=True, scheme=app.config["SCHEME"])}),
    'lug_id' : fields.Integer,
    'lug' : NestedWithEmpty({'href':fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])}),
}

class LugPickers(Resource):
    @marshal_with(lug_picker_fields)
    def get(self):
        lug_pickers = models.LugPicker.query.all()
        return lug_pickers