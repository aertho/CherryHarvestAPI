from CherryHarvestAPI import models
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources.common import tag_fields
from flask import jsonify
from flask.ext.restful import Resource, abort, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError

tag_parser = reqparse.RequestParser()
tag_parser.add_argument('epc')
tag_parser.add_argument('current_picker_number_id', int)
tag_parser.add_argument('current_lug_id', int)


class Tags(Resource):
    @marshal_with(tag_fields)
    def get(self):
        tags = models.Tag.query.all()
        return tags

    @auth.login_required
    @marshal_with(tag_fields)
    def post(self):
        args = tag_parser.parse_args()
        tag=models.Tag(epc=args['epc'])
        if args['current_picker_number_id']:
            tag.current_picker_number_id = args['current_picker_number_id']
        if args['current_lug_id']:
            tag.current_lug_id = args['current_lug_id']
        try:
            db_session.add(tag)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return jsonify(error=e, args=args), 409
        return tag


class Tag(Resource):
    @marshal_with(tag_fields)
    def get(self, epc):
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        return tag

    @auth.login_required
    @marshal_with(tag_fields)
    def patch(self, epc):
        args = tag_parser.parse_args()
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        if args['current_picker_number_id']:
            tag.current_picker_number_id = args['current_picker_number_id']
        if args['current_lug_id']:
            tag.current_lug_id = args['current_lug_id']

        db_session.commit()
        return tag

    @auth.login_required
    @marshal_with(tag_fields)
    def put(self, epc):
        args = tag_parser.parse_args()
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        if args['current_picker_number_id']:
            tag.current_picker_number_id = args['current_picker_number_id']
        else:
            tag.current_picker_number_id = None
        if args['current_lug_id']:
            tag.current_lug_id = args['current_lug_id']
        else:
            tag.current_lug_id = None
        db_session.commit()
        return tag

    @auth.login_required
    def delete(self, epc):
        tag = models.Tag.query.get(epc)
        if not tag:
            return abort(404)
        db_session.delete(tag)
        db_session.commit()
        return '', 204