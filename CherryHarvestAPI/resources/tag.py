from CherryHarvestAPI.database import db_session
from CherryHarvestAPI import models, app
from CherryHarvestAPI.resources.common import NestedWithEmpty
from CherryHarvestAPI.resources.picker import picker_fields
from flask import jsonify, request
from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError

tag_fields = {
    'epc' : fields.String,
    'current_picker_number' : NestedWithEmpty({'href' : fields.Url('picker_number', absolute=True, scheme=app.config["SCHEME"])}),
    'current_lug' : NestedWithEmpty({'href' : fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])})
}

tag_parser = reqparse.RequestParser()
tag_parser.add_argument('epc')
tag_parser.add_argument('current_picker_number_id', int)
tag_parser.add_argument('current_lug_id', int)


class Tags(Resource):
    @marshal_with(tag_fields)
    def get(self):
        tags = models.Tag.query.all()
        return tags

    @marshal_with(tag_fields)
    def post(self):
        args = tag_parser.parse_args()
        tag = models.Tag(**args)
        try:
            db_session.add(tag)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return jsonify(error=e.message), 409
        return tag


class Tag(Resource):
    @marshal_with(tag_fields)
    def get(self, epc):
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        return tag

    @marshal_with(tag_fields)
    def patch(self, epc):
        args = tag_parser.parse_args()
        print args
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        for attr, value in args.items():
            if value:
                setattr(tag, attr, value)
        if not args['current_picker_number_id']:
            tag.current_picker_number = None
        db_session.commit()
        return tag

    @marshal_with(tag_fields)
    def put(self, epc):
        args = tag_parser.parse_args()
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        for attr, value in args.items():
            setattr(tag, attr, value)
        db_session.commit()
        return tag

    def delete(self, epc):
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        db_session.delete(tag)
        db_session.commit()
        return '', 204