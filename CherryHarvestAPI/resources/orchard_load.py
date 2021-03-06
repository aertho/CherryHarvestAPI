import datetime

from CherryHarvestAPI import models
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.models import Lug
from CherryHarvestAPI.resources.common import lug_fields, orchard_load_fields
from dateutil import parser
from flask import request
from flask.ext.restful import Resource, marshal_with, reqparse, abort
from sqlalchemy.exc import IntegrityError

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
        load = models.OrchardLoad()
        if 'lugs' in request.json:
            for l in request.json['lugs']:
                lug = Lug(weight=l['weight'], block_id=l['block_id'])
                if 'lug_pickers' in l and l['lug_pickers']:
                    for lp in l['lug_pickers']:
                        if lp['picker_id'] not in [sf.picker_id for sf in lug.lug_pickers]:
                            lug.lug_pickers.append(models.LugPicker(**lp))
                        else:
                            [sf for sf in lug.lug_pickers if sf.picker_id == lp['picker_id']][0].contribution += lp['contribution']
                elif 'tag_ids' in l and l['tag_ids']:
                    for t in l['tag_ids']:
                        tag = models.Tag.query.get(t)
                        if not tag or not tag.current_picker_number or not tag.current_picker_number.picker:
                            continue
                        if tag.current_picker_number.picker_id not in [sf.picker_id for sf in lug.lug_pickers]:
                            lug.lug_pickers.append(models.LugPicker(picker_id=tag.current_picker_number.picker_id, contribution=1./len(l['tag_ids'])))
                        else:
                            [sf for sf in lug.lug_pickers if sf.picker_id == tag.current_picker_number.picker_id][0].contribution += 1./len(l['tag_ids'])
                        tag.current_picker_number = None

                load.lugs.append(lug)

        if args['departure_time']:
            try:
                load.departure_time = parser.parse(args['departure_time'])
            except ValueError:
                load.departure_time = None
        if args['arrival_time']:
            try:
                load.arrival_time = parser.parse(args['arrival_time'])
            except ValueError:
                load.arrival_time = None
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
    @marshal_with(orchard_load_fields)
    def patch(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        args = load_parser.parse_args()
        if 'lugs' in request.json and request.json['lugs']:
            for l in request.json['lugs']:
                if 'lug_pickers' in l and l['lug_pickers']:
                    lps = []
                    for lp in l['lug_pickers']:
                        if lp['picker_id'] not in [sf.picker_id for sf in lps]:
                            lps.append(models.LugPicker(**lp))
                        else:
                            [sf for sf in lps if sf.picker_id == lp['picker_id']][0].contribution += lp['contribution']
                    l['lug_pickers'] = lps
            args['lugs'] = [Lug.query.get(l['id']) if 'id' in l and Lug.query.get(l['id']) else Lug(**l) for l in request.json['lugs']]
        else:
            args['lugs'] = []

        for attr, value in args.items():
            if value:
                setattr(load, attr, value)
        if load.departure_time:
            try:
                load.departure_time = parser.parse(load.departure_time)
            except ValueError:
                load.departure_time = datetime.datetime.now()
        if load.arrival_time:
            try:
                load.arrival_time = parser.parse(load.arrival_time)
            except ValueError:
                load.arrival_time = datetime.datetime.now()
        try:
            db_session.add(load)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return {'error' : e.message}, 409
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
    @marshal_with(lug_fields)
    def get(self, id):
        load = models.OrchardLoad.query.get(id)
        if not load:
            return abort(404)
        return load.lugs