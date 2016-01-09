import json
from datetime import datetime

from CherryHarvestAPI import app
from CherryHarvestAPI.database import db_session, destroy_db, init_db
from CherryHarvestAPI.models import Lug, Picker, Block, OrchardLoad, FarmLoad
from flask.ext.testing import TestCase


class BaseViewsTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True

        return app

    def setUp(self):
        init_db()

    def tearDown(self):
        db_session.remove()
        destroy_db()

    def create_lug(self, weight=10.0, current_status='orchard', picker=None, block=None, orchard_load=None, farm_load=None):
        if not picker:
            picker = self.create_picker()
        if not block:
            block = self.create_block()
        if not orchard_load:
            orchard_load = self.create_orchard_load()
        if not farm_load:
            farm_load = self.create_farm_load()
        l = Lug(weight=weight, current_status=current_status, picker=picker, block=block, orchard_load=orchard_load, farm_load=farm_load)
        db_session.add(l)
        db_session.commit()
        return l

    def create_picker(self, first_name='Alec', last_name='Thomas', pay_rate=25.5, pay_type='time', mobile_number='0427440201', email='alecthomas3@gmail.com'):
        p = Picker(first_name = first_name, last_name = last_name, pay_rate = pay_rate, pay_type = pay_type, mobile_number = mobile_number, email = email)
        db_session.add(p)
        db_session.commit()
        return p

    def create_block(self, variety = 'Simone', plant_year = '2007', orientation = 'N'):
        b = Block(variety = variety, plant_year = plant_year, orientation = orientation)
        db_session.add(b)
        db_session.commit()
        return b

    def create_orchard_load(self, date_time = None):
        if not date_time:
            date_time = datetime.now()
        o = OrchardLoad(date_time = date_time)
        db_session.add(o)
        db_session.commit()
        return o

    def create_farm_load(self, date_time = None):
        if not date_time:
            date_time = datetime.now()
        f = FarmLoad(date_time = date_time)
        db_session.add(f)
        db_session.commit()
        return f


class LugsTestCase(BaseViewsTestCase):
    def test_get_lugs(self):
        l = self.create_lug()
        r = self.client.get('http://localhost:8943/lugs')
        self.assertEqual(r.status_code,200)
        self.assertEqual(l.serialize(),r.json['lugs'][0])

    def test_post_lugs(self):
        data = dict(lug = {
            'weight' : 10.0,
            'current_status' : 'orchard'
        })
        r = self.client.post('http://localhost:8943/lugs', data=json.dumps(data), content_type='application/json')
        self.assertEqual(r.status_code,201)
        self.assertTrue(Lug.query.filter_by(**data['lug']).first())

    def test_post_lugs_with_invalid_arguments(self):
        data = dict(lug = {
            'weighdt' : 10.0,
            'current_status' : 'orchard'
        })
        r = self.client.post('http://localhost:8943/lugs', data=json.dumps(data), content_type='application/json')
        self.assertEqual(r.status_code,406)
        self.assertIn('error', r.json)

class LugTestCase(BaseViewsTestCase):
    def test_get_lug(self):
        l = self.create_lug()
        r = self.client.get('http://localhost:8943/lugs/{}'.format(l.id))
        self.assertEqual(r.status_code,200)
        self.assertEqual(l.deep_serialize(),r.json['lug'])

    def test_patch_lug(self):
        data = dict(lug = {
            'weight' : 10.0,
            'current_status' : 'farm'
        })
        l = self.create_lug()
        r = self.client.patch('/lugs/{}'.format(l.id), data=json.dumps(data), content_type='application/json')
        self.assertEqual(r.status_code,200)
        self.assertTrue(Lug.query.filter_by(**data['lug']).first())
        self.assertFalse(Lug.query.filter_by(current_status='orchard').first())
