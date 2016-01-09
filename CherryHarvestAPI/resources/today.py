from datetime import date

from CherryHarvestAPI.models import OrchardLoad
from flask.ext.restful import Resource
from sqlalchemy.orm import Load


class Today(Resource):
    def get(self):
        total = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == date.today()])
        return {'total' : total}