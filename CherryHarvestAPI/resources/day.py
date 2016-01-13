import datetime

import dateutil
from CherryHarvestAPI.models import OrchardLoad, Lug, Block, Picker
from dateutil import parser
from flask import url_for, redirect
from flask.ext.restful import Resource
from CherryHarvestAPI import app

def ranked_pickers(date):
    return [{'name':'{} {}'.format(p.first_name, p.last_name),
                       'total':p.daily_total(date),
                       'rank':i,
                       'picker_numbers':[pn.id for pn in p.picker_numbers]}
            for i, p in enumerate(sorted(Picker.query.all(), key=lambda x: x.daily_total(date), reverse=True),1)
            if p.daily_total(date) and not p.is_manager]

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
    def get(self, date):
        date = dateutil.parser.parse(date).date()
        blocks = [{'variety' : b.variety, 'weight': b.daily_total(date)} for b in Block.query.all() if b.daily_total(date)]
        total = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == date])
        loads = [{'time' :str(l.arrival_time), 'weight' : l.net_weight} for l in OrchardLoad.query.order_by(OrchardLoad.arrival_time).all() if l.arrival_time.date() == date]
        pickers = ranked_pickers(date)
        return {'total' : total,
                'blocks': blocks,
                'loads': loads,
                'pickers' : pickers}


class Today(Resource):
    def get(self):
        return redirect(url_for('day', date=str(datetime.date.today())))

class Yesterday(Resource):
    def get(self):
        return redirect(url_for('day', date=str((datetime.datetime.now() - datetime.timedelta(days=1)).date())))