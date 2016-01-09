from copy import copy

from CherryHarvestAPI import models
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources import load
from CherryHarvestAPI.resources.common import simple_lug_fields
from dateutil import parser
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
import regex

_farm_load_fields = copy(load.outer_load_fields)
# _farm_load_fields['lugs'].endpoint = 'farm_load_lugs'



class FarmLoads(load.Loads):
    farm_load_fields = _farm_load_fields

    @marshal_with(_farm_load_fields)
    def get(self):
        loads = models.FarmLoad.query.all()
        return loads

    @marshal_with(farm_load_fields)
    def post(self):
        args = self.load_parser.parse_args()
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
    
class FarmLoad(load.Load):
    farm_load_fields = _farm_load_fields

    @marshal_with(_farm_load_fields)
    def get(self, id):
        load = models.FarmLoad.query.get(id)
        if not load:
            return abort(404)
        return load

    def delete(self, id):
        load = models.FarmLoad.query.get(id)
        if not load:
            return abort(404)
        db_session.delete(load)
        db_session.commit()
        return '', 204

class FarmLoadLugs(load.LoadLugs):
    @marshal_with(simple_lug_fields)
    def get(self, id):
        load = models.FarmLoad.query.get(id)
        if not load:
            return abort(404)
        return load.lugs