import datetime

from CherryHarvestAPI.models import OrchardLoad, Block, Picker
from CherryHarvestAPI.resources.common import totalled_blocks, ranked_pickers
from CherryHarvestAPI.resources.day import period_fields
from flask import url_for, redirect
from flask.ext.restful import Resource, marshal_with


def season(year):
    total = sum([l.total for l in OrchardLoad.query.all() if l.arrival_time.date().year == year])
    blocks = totalled_blocks(lambda b: Block.seasonal_total(b, year=year))
    orchard_loads = [l for l in OrchardLoad.query.order_by(OrchardLoad.arrival_time).all() if
                     l.arrival_time.date().year == year]
    pickers = ranked_pickers(lambda p: Picker.seasonal_total(p, datetime.date(year, 12, 31)))
    return {'total' : total,
            'totalled_blocks': blocks,
            'orchard_loads': orchard_loads,
            'ranked_pickers' : pickers}

class Seasons(Resource):
    @marshal_with(period_fields)
    def get(self):
        years = [2016]
        return [season(y) for y in years]

class Season(Resource):
    @marshal_with(period_fields)
    def get(self, year):
        return season(year)

class CurrentSeason(Resource):
    def get(self):
        return redirect(url_for('season', year=datetime.date.today().year))