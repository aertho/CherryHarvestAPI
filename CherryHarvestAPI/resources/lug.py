from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI import models, app
from CherryHarvestAPI.resources.common import NestedWithEmpty
from CherryHarvestAPI.resources.picker import picker_fields
from flask import jsonify, request
from flask.ext.restful import Resource, abort, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

lug_fields = {
    'id' : fields.Integer,
    'weight' : fields.String,
    'current_status' : fields.String,
    # 'lug_pickers' : fields.Url('lug_pickers', absolute=True, scheme=app.config["SCHEME"]),
    'block_id' : fields.Integer,
    'block' : NestedWithEmpty({'href' : fields.Url('block', absolute=True, scheme=app.config["SCHEME"])}),
    'orchard_load_id' : fields.Integer,
    'orchard_load' : NestedWithEmpty({'href' : fields.Url('orchard_load', absolute=True, scheme=app.config["SCHEME"])}),
    'farm_load_id' : fields.Integer,
    'farm_load' : NestedWithEmpty({'href' : fields.Url('farm_load', absolute=True, scheme=app.config["SCHEME"])}),
}

lug_picker_fields = {
    'contribution' : fields.Float,
    'picker' : NestedWithEmpty({'href' : fields.Url('picker', absolute=True, scheme=app.config["SCHEME"])}),
    'lug' : NestedWithEmpty({'href':fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])}),
}

def picker_id(value):
    if not models.Picker.query.get(value):
        raise ValueError("{} is not a valid picker id.".format(value))
    return value

def block_id(value):
    if not models.Block.query.get(value):
        raise ValueError("{} is not a valid block id.".format(value))
    return value

def farm_load_id(value):
    if not models.FarmLoad.query.get(value):
        raise ValueError("{} is not a valid farm load id.".format(value))
    return value

def orchard_load_id(value):
    if not models.OrchardLoad.query.get(value):
        raise ValueError("{} is not a valid orchard load id.".format(value))
    return value

lug_parser = reqparse.RequestParser()
lug_parser.add_argument('id', int)
lug_parser.add_argument('weight', float)
lug_parser.add_argument('current_status')
lug_parser.add_argument('block_id', int)
lug_parser.add_argument('farm_load_id', int)
lug_parser.add_argument('orchard_load_id', int)

lug_picker_parser = reqparse.RequestParser()
lug_picker_parser.add_argument('contribution', type=float)
lug_picker_parser.add_argument('picker_id', type=int)
lug_picker_parser.add_argument('lug_id', type=int)

class Lugs(Resource):
    @marshal_with(lug_fields)
    def get(self):
        lugs = models.Lug.query.all()
        return lugs

    @auth.login_required
    @marshal_with(lug_fields)
    def post(self):
        args = lug_parser.parse_args()
        lug = models.Lug(**args)
        try:
            db_session.add(lug)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return jsonify(error=e.message), 409
        return lug


class Lug(Resource):
    @marshal_with(lug_fields)
    def get(self, id):
        lug = models.Lug.query.get(id)
        if not lug:
            return abort(404)
        return lug

    @auth.login_required
    @marshal_with(lug_fields)
    def patch(self, id):
        args = lug_parser.parse_args()
        lug = models.Lug.query.get(id)
        if not lug:
            return abort(404)
        for attr, value in args.items():
            if value:
                setattr(lug, attr, value)
        db_session.commit()
        return lug

    @auth.login_required
    @marshal_with(lug_fields)
    def put(self, id):
        args = lug_parser.parse_args()
        lug = models.Lug.query.get(id)
        if not lug:
            return abort(404)
        for attr, value in args.items():
            setattr(lug, attr, value)
        db_session.commit()
        return lug

    @auth.login_required
    def delete(self, id):
        lug = models.Lug.query.get(id)
        if not lug:
            return abort(404)
        db_session.delete(lug)
        db_session.commit()
        return '', 204

class LugPickers(Resource):
    @marshal_with(lug_picker_fields)
    def get(self, id):
        lug = models.Lug.query.get(id)
        if not lug:
            return abort(404)
        return lug.lug_pickers

    @auth.login_required
    @marshal_with(lug_picker_fields)
    def post(self, id):
        args = lug_picker_parser.parse_args()
        lug = models.Lug.query.get(id)
        if not lug:
            return abort(404)
        lug.lug_pickers.append(models.LugPicker(**args))
        try:
            db_session.commit()
        except (IntegrityError, FlushError), e:
            db_session.rollback()
            lp = [l for l in lug.lug_pickers if l.picker_id == args['picker_id']][0]
            lp.contribution += args['contribution']
            db_session.commit()

            return jsonify(error=e.message), 409
        return lug.lug_pickers