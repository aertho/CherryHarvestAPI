import datetime

import dateutil
from CherryHarvestAPI.models import OrchardLoad, Lug, Block, Picker
from dateutil import parser
from flask import url_for, redirect
from flask.ext.restful import Resource
from CherryHarvestAPI import app

def ranked_pickers():
    return [{'name':'{} {}'.format(p.first_name, p.last_name),
                       'total':p.total,
                       'rank':i,
                       'picker_numbers':[pn.id for pn in p.picker_numbers]}
            for i, p in enumerate(sorted(Picker.query.all(), key=lambda x: x.total, reverse=True),1)
            if p.total]

class Seasons(Resource):
    def get(self):
        years = [2016]
        return [{
            'season' : y,
            'total' : sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date().year == y]),
            'pickers' : ranked_pickers()[:min(3,len(ranked_pickers()))],
            'href' : url_for('season', year=y, _external=True, _scheme=app.config['SCHEME'])
        } for y in years]

class Season(Resource):
    def get(self, year):
        blocks = [{'variety' : b.variety, 'weight': b.total} for b in Block.query.all() if b.total]
        total = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date().year == year])
        # loads = [{'time' :str(l.arrival_time), 'weight' : l.net_weight} for l in OrchardLoad.query.order_by(OrchardLoad.arrival_time).all() if l.arrival_time.date().year == year]
        pickers = ranked_pickers()
        return {'total' : total,
                'blocks': blocks,
                # 'loads': loads,
                'pickers' : pickers}

class CurrentSeason(Resource):
    def get(self):
        return redirect(url_for('season', year=datetime.date.today().year))