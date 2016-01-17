import datetime

import dateutil
from CherryHarvestAPI.models import OrchardLoad, Lug, Block, Picker
from CherryHarvestAPI.resources.block import block_fields
from CherryHarvestAPI.resources.common import ranked_pickers, totalled_blocks
from CherryHarvestAPI.resources.orchard_load import orchard_load_fields
from CherryHarvestAPI.resources.picker import ranked_picker_fields
from dateutil import parser
from flask import url_for, redirect
from flask.ext.restful import Resource, fields, marshal_with
from CherryHarvestAPI import app, models

totalled_block_fields = {
    'total' : fields.Integer,
    'block' : fields.Nested(block_fields)
}

day_fields = {
    'total' : fields.Integer,
    'totalled_blocks' : fields.Nested(totalled_block_fields),
    'orchard_loads' : fields.Nested(orchard_load_fields),
    'ranked_pickers' : fields.Nested(ranked_picker_fields),
}

class Days(Resource):
    def get(self):
        dates = set([ol.arrival_time.date() for ol in OrchardLoad.query.all()])
        return [{
            'date' : str(d),
            'total' : sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == d]),
            'pickers' : ranked_pickers(d)[:min(3,len(ranked_pickers(d)))],
            'href' : url_for('day', date=str(d), _external=True, _scheme=app.config['SCHEME'])
        } for d in dates]


class Day(Resource):
    @marshal_with(day_fields)
    def get(self, date):
        date = dateutil.parser.parse(date).date()
        total = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == date])
        blocks = totalled_blocks(date=date)
        orchard_loads = [l for l in OrchardLoad.query.order_by(OrchardLoad.arrival_time).all() if
                         l.arrival_time.date() == date]
        pickers = ranked_pickers(date=date)
        return {'total' : total,
                'totalled_blocks': blocks,
                'orchard_loads': orchard_loads,
                'ranked_pickers' : pickers}

class Today(Resource):
    def get(self):
        return redirect(url_for('day', date=str(datetime.date.today())))

class Yesterday(Resource):
    def get(self):
        return redirect(url_for('day', date=str((datetime.datetime.now() - datetime.timedelta(days=1)).date())))