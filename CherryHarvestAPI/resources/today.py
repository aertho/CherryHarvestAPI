from datetime import date, datetime

import pytz
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.models import OrchardLoad, Lug, Block, Picker
from flask.ext.restful import Resource
from sqlalchemy.orm import Load


class Today(Resource):
    @auth.login_required
    def get(self):
        blocks = [{'variety' : b.variety, 'weight_today': sum([l.weight for l in Lug.query.all() if l.block_id == b.id and l.orchard_load.arrival_time.today() == date.today()])} for b in Block.query.all()]
        total_today = sum([l.net_weight for l in OrchardLoad.query.all() if l.arrival_time.date() == datetime.now(pytz.timezone('Australia/Hobart')).date()])
        loads = [{'time' :str(l.arrival_time), 'weight' : l.net_weight} for l in OrchardLoad.query.all() if l.arrival_time.date() == date.today()]
        pickers = sorted([{'name':'{} {}'.format(p.first_name, p.last_name), 'weight':p.daily_total()} for p in Picker.query.all() if p.daily_total()], key=lambda x: -x['weight'])
        return {'total_today' : total_today,
                'blocks': blocks,
                'loads': loads,
                'pickers' : pickers}