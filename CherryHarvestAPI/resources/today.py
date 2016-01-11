from datetime import date, datetime

import pytz
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.models import OrchardLoad, Lug, Block, Picker
from flask.ext.restful import Resource
from sqlalchemy.orm import Load


class Today(Resource):
    @auth.login_required
    def get(self):
        blocks = [{'variety' : b.variety, 'weight_today': b.today_total} for b in Block.query.all() if b.today_total]
        total_today = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == date.today()])
        loads = [{'time' :str(l.arrival_time), 'weight' : l.net_weight} for l in OrchardLoad.query.order_by(OrchardLoad.arrival_time).all() if l.arrival_time.date() == date.today()]
        pickers = [{'name':'{} {}'.format(p.first_name, p.last_name), 'weight':p.daily_total(), 'rank':i, 'picker_numbers':[pn.id for pn in p.picker_numbers]} for i, p in enumerate(sorted(Picker.query.all(), key=Picker.daily_total, reverse=True),1) if p.daily_total()]
        return {'total_today' : total_today,
                'blocks': blocks,
                'loads': loads,
                'pickers' : pickers}