from CherryHarvestAPI.database import db_session
from CherryHarvestAPI import models, app
from CherryHarvestAPI.resources.common import NestedWithEmpty
from CherryHarvestAPI.resources.picker import picker_fields
from flask import jsonify, request
from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

lug_picker_fields = {
    'picker' : NestedWithEmpty({'href' : fields.Url('picker', absolute=True, scheme=app.config["SCHEME"])}),
    'lug' : NestedWithEmpty({'href' : fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])}),
    'contribution' : fields.Float
}

lug_picker_parser = reqparse.RequestParser()
lug_picker_parser.add_argument('lug_id', int)
lug_picker_parser.add_argument('picker_id', int)
lug_picker_parser.add_argument('contribution', float)


class LugPickers(Resource):
    @marshal_with(lug_picker_fields)
    def get(self):
        lug_pickers = models.LugPicker.query.all()
        return lug_pickers

    @marshal_with(lug_picker_fields)
    def post(self):
        args = lug_picker_parser.parse_args()
        lug_picker = models.LugPicker(**args)
        try:
            db_session.add(lug_picker)
            db_session.commit()
        except (IntegrityError, FlushError), e:
            db_session.rollback()
            return jsonify(error=e.message), 409
        return lug_picker


class LugPicker(Resource):
    @marshal_with(lug_picker_fields)
    def get(self, lug_id, picker_id):
        lug_picker = models.LugPicker.query.get(lug_id, picker_id)
        if not lug_picker:
            return abort(404)
        return lug_picker

    @marshal_with(lug_picker_fields)
    def patch(self, lug_id, picker_id):
        args = lug_picker_parser.parse_args()
        lug_picker = models.LugPicker.query.get(lug_id, picker_id)
        if not lug_picker:
            return abort(404)
        for attr, value in args.items():
            if value:
                setattr(lug_picker, attr, value)
        db_session.commit()
        return lug_picker

    @marshal_with(lug_picker_fields)
    def put(self, lug_id, picker_id):
        args = lug_picker_parser.parse_args()
        lug_picker = models.LugPicker.query.get(lug_id. picker_id)
        if not lug_picker:
            return abort(404)
        for attr, value in args.items():
            setattr(lug_picker, attr, value)
        db_session.commit()
        return lug_picker

    def delete(self, lug_id, picker_id):
        lug_picker = models.LugPicker.query.get(lug_id, picker_id)
        if not lug_picker:
            return abort(404)
        db_session.delete(lug_picker)
        db_session.commit()
        return '', 204