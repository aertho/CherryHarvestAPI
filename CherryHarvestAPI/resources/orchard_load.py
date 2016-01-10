from copy import copy

from CherryHarvestAPI import models
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.models import Lug
from CherryHarvestAPI.resources.common import simple_lug_fields
from dateutil import parser
from flask import json, request
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
import regex

orchard_load_fields = {
    'id' : fields.Integer,
    'net_weight' : fields.Float,
    'departure_time' : fields.DateTime,
    'arrival_time' : fields.DateTime,
    # 'destination' : fields.String,
    # 'lugs' : fields.Url('load_lugs', absolute=True, scheme=app.config['SCHEME'])
}

load_parser = reqparse.RequestParser()
load_parser.add_argument('id', type=int)
load_parser.add_argument('departure_time')
load_parser.add_argument('arrival_time')

class OrchardLoads(Resource):
    orchard_load_fields = orchard_load_fields

    @marshal_with(orchard_load_fields)
    def get(self):
        loads = models.OrchardLoad.query.all()
        return loads

    @auth.login_required
    @marshal_with(orchard_load_fields)
    def post(self):
        args = load_parser.parse_args()
        if 'lugs' in request.json and request.json['lugs']:
            args['lugs'] = [Lug(**l) for l in request.json['lugs']]
        else:
            args['lugs'] = []
        load = models.OrchardLoad(**args)
        if load.departure_time:
            load.departure_time = parser.parse(load.departure_time)
        if load.arrival_time:
            load.arrival_time = parser.parse(load.arrival_time)
        try:
            db_session.add(load)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return {'error' : e.message}, 409
        return load
    
class OrchardLoad(Resource):
    orchard_load_fields = orchard_load_fields

    @marshal_with(orchard_load_fields)
    def get(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        return load

    @auth.login_required
    def delete(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        db_session.delete(load)
        db_session.commit()
        return '', 204

class OrchardLoadLugs(Resource):
    @marshal_with(simple_lug_fields)
    def get(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        return load.lugs