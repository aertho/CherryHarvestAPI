from datetime import date

from CherryHarvestAPI.models import OrchardLoad, Lug, Block
from flask.ext.restful import Resource
from sqlalchemy.orm import Load


class Today(Resource):
    def get(self):
        block_totals = {b.variety: sum([l.weight for l in Lug.query.all() if l.block == b and l.orchard_load.arrival_time == date.today()]) for b in Block.query.all()}
        total = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == date.today()])
        return {'total' : total,
                'block_totals': block_totals}