from CherryHarvestAPI import models
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources.common import farm_load_fields, lug_fields
from dateutil import parser
from flask.ext.restful import Resource, marshal_with, reqparse, abort
from sqlalchemy.exc import IntegrityError

load_parser = reqparse.RequestParser()
load_parser.add_argument('id', type=int)
load_parser.add_argument('departure_time')
load_parser.add_argument('arrival_time')

class FarmLoads(Resource):
    farm_load_fields = farm_load_fields

    @marshal_with(farm_load_fields)
    def get(self):
        loads = models.FarmLoad.query.all()
        return loads

    @auth.login_required
    @marshal_with(farm_load_fields)
    def post(self):
        args = load_parser.parse_args()
        load = models.FarmLoad(**args)
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
    
class FarmLoad(Resource):
    farm_load_fields = farm_load_fields

    @marshal_with(farm_load_fields)
    def get(self, id):
        load = models.FarmLoad.query.get(id)
        if not load:
            return abort(404)
        return load

    @auth.login_required
    def delete(self, id):
        load = models.FarmLoad.query.get(id)
        if not load:
            return abort(404)
        db_session.delete(load)
        db_session.commit()
        return '', 204

class FarmLoadLugs(Resource):
    @marshal_with(lug_fields)
    def get(self, id):
        load = models.FarmLoad.query.get(id)
        if not load:
            return abort(404)
        return load.lugs