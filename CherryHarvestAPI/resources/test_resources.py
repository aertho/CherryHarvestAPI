import json
from datetime import datetime

from CherryHarvestAPI import app
from CherryHarvestAPI.database import db_session, destroy_db, init_db
from CherryHarvestAPI.models import Lug, Picker, Block, OrchardLoad, FarmLoad
from flask.ext.testing import TestCase


class BaseResourcesTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

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

    def create_block(self, variety = 'Simone', plant_year = '2007'):
        b = Block(variety = variety, plant_year = plant_year)
        db_session.add(b)
        db_session.commit()
        return b

    def create_orchard_load(self, arrival_time=None, departure_time=None):
        if not arrival_time:
            arrival_time = datetime.now()
        if not departure_time:
            departure_time = datetime.now()
        o = OrchardLoad(arrival_time = arrival_time, departure_time = departure_time)
        db_session.add(o)
        db_session.commit()
        return o

    def create_farm_load(self, arrival_time=None, departure_time=None):
        if not arrival_time:
            arrival_time = datetime.now()
        if not departure_time:
            departure_time = datetime.now()
        f = FarmLoad(arrival_time = arrival_time, departure_time = departure_time)
        db_session.add(f)
        db_session.commit()
        return f

class LugResourceTestCase(BaseResourcesTestCase):
    def test_get_lugs(self):
        l = self.create_lug()
        m = self.create_lug()
        r = self.client.get('/lugs', follow_redirects=True)
        self.assert200(r)
        self.assertEqual(l.id, r.json[0]['id'])
        self.assertEqual(m.id, r.json[1]['id'])

    def test_get_lug(self):
        l = self.create_lug()
        r = self.client.get('/lugs/{}'.format(l.id), follow_redirects=True)
        self.assert200(r)
        self.assertEqual(l.id,r.json['id'])
        self.assertEqual(l.current_status,r.json['current_status'])

    def test_post_lug(self):
        data = {
            'weight' : 10.0,
            'current_status' : 'orchard',
        }
        r = self.client.post('/lugs/', data=json.dumps(data), content_type='application/json')
        self.assert200(r)
        self.assertTrue(Lug.query.filter_by(**data).first())

    def test_patch_lug(self):
        data = {
            'weight' : 11.0,
            'current_status' : 'farm',
        }
        l = self.create_lug()
        r = self.client.patch('/lugs/{}'.format(l.id), data=json.dumps(data), content_type='application/json')
        l = Lug.query.get(l.id)
        self.assert200(r)
        self.assertEqual(l.weight, data['weight'])
        self.assertTrue(l.picker_id)

    def test_put_lug(self):
        data = {
            'weight' : 11.0,
            'current_status' : 'farm',
        }
        l = self.create_lug()
        r = self.client.put('/lugs/{}'.format(l.id), data=json.dumps(data), content_type='application/json')
        l = Lug.query.get(l.id)
        self.assert200(r)
        self.assertEqual(l.weight, data['weight'])
        self.assertFalse(l.picker_id)

    def test_delete_lug(self):
        l = self.create_lug()
        r = self.client.delete('/lugs/{}'.format(l.id))
        self.assertEqual(r.status_code, 204)
        self.assertFalse(Lug.query.get(l.id))

class FarmLoadResourceTestCase(BaseResourcesTestCase):
    def setUp(self):
        BaseResourcesTestCase.setUp(self)
        self.farm_load=self.create_farm_load()

    def test_get_farm_loads(self):
        r = self.client.get('/farm-loads/', follow_redirects=True)
        self.assert200(r)
        self.assertEqual(self.farm_load.id, r.json[0]['id'])

    def test_get_farm_load(self):
        r = self.client.get('/farm-loads/{}/'.format(self.farm_load.id), follow_redirects=True)
        self.assert200(r)
        self.assertEqual(self.farm_load.id, r.json['id'])


    def test_get_lugs_subcollection(self):
        r = self.client.get('/farm_loads/{}/lugs/'.format(self.farm_load.id))
        self.assertEqual(r.json[0]['id'], self.farm_load.lugs[0].id)