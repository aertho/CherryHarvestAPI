from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI import models, app
from CherryHarvestAPI.models import Tag
from CherryHarvestAPI.resources.common import NestedWithEmpty
from CherryHarvestAPI.resources.picker import picker_fields
from flask import jsonify, request
from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError

picker_number_fields = {
    'id' : fields.Integer,
    'picker' : NestedWithEmpty({'href' : fields.Url('picker', absolute=True, scheme=app.config["SCHEME"])}),
    'card_count' : fields.Integer,
}

picker_number_parser = reqparse.RequestParser()
picker_number_parser.add_argument('id', type=int)
picker_number_parser.add_argument('picker_id', type=int)


class PickerNumbers(Resource):
    @marshal_with(picker_number_fields)
    def get(self):
        picker_numbers = models.PickerNumber.query.all()
        return picker_numbers

    @auth.login_required
    @marshal_with(picker_number_fields)
    def post(self):
        args = picker_number_parser.parse_args()
        picker_number = models.PickerNumber(**args)
        try:
            db_session.add(picker_number)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return jsonify(error=e.message), 409
        return picker_number


class PickerNumber(Resource):
    @marshal_with(picker_number_fields)
    def get(self, id):
        picker_number = models.PickerNumber.query.get(id)
        if not picker_number:
            return abort(404)
        return picker_number

    @auth.login_required
    @marshal_with(picker_number_fields)
    def patch(self, id):
        args = picker_number_parser.parse_args()
        picker_number = models.PickerNumber.query.get(id)
        if not picker_number:
            return abort(404)
        if 'tags' in request.json and request.json['tag_epcs']:
            for e in request.json['tag_epcs']:
                tag = models.Tag.query.get(e)
                if not tag:
                    tag = Tag(epc=e)
                picker_number.current_cards.append(tag)
        for attr, value in args.items():
            if value:
                setattr(picker_number, attr, value)
        db_session.commit()
        return picker_number

    @auth.login_required
    @marshal_with(picker_number_fields)
    def put(self, id):
        args = picker_number_parser.parse_args()
        picker_number = models.PickerNumber.query.get(id)
        if not picker_number:
            return abort(404)
        for attr, value in args.items():
            setattr(picker_number, attr, value)
        db_session.commit()
        return picker_number

    @auth.login_required
    def delete(self, id):
        picker_number = models.PickerNumber.query.get(id)
        if not picker_number:
            return abort(404)
        db_session.delete(picker_number)
        db_session.commit()
        return '', 204