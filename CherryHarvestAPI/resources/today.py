from datetime import date

from CherryHarvestAPI.models import OrchardLoad, Lug, Block, Picker
from flask.ext.restful import Resource
from sqlalchemy.orm import Load


class Today(Resource):
    def get(self):
        block_totals = [{b.variety: sum([l.weight for l in Lug.query.all() if l.block == b and l.orchard_load.arrival_time == date.today()])} for b in Block.query.all()]
        total = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == date.today()])
        load_times = len([l for l in OrchardLoad.query.all() if l.arrival_time.date() == date.today()])
        pickers = [{'{} {}'.format(p.first_name, p.last_name): p.daily_total()} for p in Picker.query.all() if p.daily_total()]
        return {'total' : total,
                'block_totals': block_totals,
                'load_times': load_times,
                'pickers' : pickers}