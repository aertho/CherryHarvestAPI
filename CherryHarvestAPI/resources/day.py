import datetime

import dateutil
from CherryHarvestAPI import app
from CherryHarvestAPI.models import OrchardLoad
from CherryHarvestAPI.resources.common import ranked_pickers, totalled_blocks, period_fields
from dateutil import parser
from flask import url_for, redirect
from flask.ext.restful import Resource, marshal_with


class Days(Resource):
    def get(self):
        dates = set([ol.arrival_time.date() for ol in OrchardLoad.query.all()])
        return [{
            'date' : str(d),
            'total' : sum([l.total for l in OrchardLoad.query.all() if l.arrival_time.date() == d]),
            'pickers' : ranked_pickers(d)[:min(3,len(ranked_pickers(d)))],
            'href' : url_for('day', date=str(d), _external=True, _scheme=app.config['SCHEME'])
        } for d in dates]


class Day(Resource):
    @marshal_with(period_fields)
    def get(self, date):
        date = dateutil.parser.parse(date).date()
        total = sum([l.total for l in OrchardLoad.query.all() if l.arrival_time.date() == date])
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