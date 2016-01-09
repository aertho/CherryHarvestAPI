import datetime

from CherryHarvestAPI import models, app
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources.common import simple_lug_fields
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
from dateutil import parser

outer_load_fields = {
    'id' : fields.Integer,
    'net_weight' : fields.Float,
    'departure_time' : fields.DateTime,
    'arrival_time' : fields.DateTime,
    # 'destination' : fields.String,
    # 'lugs' : fields.Url('load_lugs', absolute=True, scheme=app.config['SCHEME'])
}
outer_load_parser = reqparse.RequestParser()
outer_load_parser.add_argument('departure_time')
outer_load_parser.add_argument('arrival_time')

class Loads(Resource):

    load_fields = outer_load_fields
    load_parser = outer_load_parser

    @marshal_with(load_fields)
    def get(self):
        loads = models.Load.query.all()
        return loads

    @marshal_with(outer_load_fields)
    def post(self):
        args = self.load_parser.parse_args()
        load = models.Load(**args)
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
    
class Load(Resource):

    load_fields = outer_load_fields
    load_parser = outer_load_parser

    @marshal_with(load_fields)
    def get(self, id):
        load = models.Load.query.get(id)
        if not load:
            return abort(404)
        return load

    @marshal_with(load_fields)
    def patch(self, id):
        args = self.load_parser.parse_args()
        load = models.Load.query.get(id)
        if not load:
            return abort(404)
        for attr, value in args.items():
            if value:
                setattr(load, attr, value)
        db_session.commit()
        return load

    @marshal_with(load_fields)
    def put(self, id):
        args = self.load_parser.parse_args()
        load = models.Load.query.get(id)
        if not load:
            return abort(404)
        for attr, value in args.items():
            setattr(load, attr, value)
        db_session.commit()
        return load

    def delete(self, id):
        load = models.Load.query.get(id)
        if not load:
            return abort(404)
        db_session.delete(load)
        db_session.commit()
        return '', 204

class LoadLugs(Resource):
    @marshal_with(simple_lug_fields)
    def get(self, id):
        load = models.Load.query.get(id)
        if not load:
            return abort(404)
        return load.lugs