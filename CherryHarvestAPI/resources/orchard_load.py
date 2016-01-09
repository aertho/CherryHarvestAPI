from copy import copy

from CherryHarvestAPI import models
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources import load
from dateutil import parser
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
import regex

_orchard_load_fields = copy(load.outer_load_fields)
# _orchard_load_fields['lugs'].endpoint = 'orchard_load_lugs'



class OrchardLoads(load.Loads):
    orchard_load_fields = _orchard_load_fields

    @marshal_with(_orchard_load_fields)
    def get(self):
        loads = models.OrchardLoad.query.all()
        return loads

    @marshal_with(orchard_load_fields)
    def post(self):
        args = self.load_parser.parse_args()
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
    
class OrchardLoad(load.Load):
    orchard_load_fields = _orchard_load_fields

    @marshal_with(_orchard_load_fields)
    def get(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        return load

    def delete(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        db_session.delete(load)
        db_session.commit()
        return '', 204

class OrchardLoadLugs(load.LoadLugs):
    pass