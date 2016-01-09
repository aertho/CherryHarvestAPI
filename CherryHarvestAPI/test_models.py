import json
from datetime import datetime

from CherryHarvestAPI import app
from CherryHarvestAPI.database import db_session, destroy_db, init_db
from CherryHarvestAPI.models import Lug, Picker, Block, OrchardLoad, FarmLoad, Tag, LugPicker
from flask.ext.testing import TestCase


class BaseModelsTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True

        return app

    def setUp(self):
        destroy_db()
        init_db()

    def tearDown(self):
        db_session.remove()

    def create_lug(self, weight=10.0, current_status='orchard', block=None, orchard_load=None, farm_load=None):
        if not block:
            block = self.create_block()
        if not orchard_load:
            orchard_load = self.create_orchard_load()
        if not farm_load:
            farm_load = self.create_farm_load()
        l = Lug(weight=weight, current_status=current_status,block=block, orchard_load=orchard_load, farm_load=farm_load)
        self.create_lug_picker_association(lug=l)

        db_session.add(l)
        db_session.commit()
        return l

    def create_picker(self, first_name='Alec', last_name='Thomas', pay_rate=25.5, pay_type='time', mobile_number='0427440201', email='alecthomas3@gmail.com'):
        p = Picker(first_name = first_name, last_name = last_name, pay_rate = pay_rate, pay_type = pay_type, mobile_number = mobile_number, email = email)
        db_session.add(p)
        db_session.commit()
        return p

    def create_block(self, variety = 'Simone', plant_year = '2007', orientation = 'north'):
        b = Block(variety = variety, plant_year = plant_year, orientation = orientation)
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

    def create_rfid_card(self, epc='1', current_lug=None, current_picker=None):
        if not current_lug:
            current_lug = self.create_lug()
        if not current_picker:
            current_picker = self.create_picker()

        rc = Tag(epc=epc, current_lug=current_lug, current_picker=current_picker)
        db_session.add(rc)
        db_session.commit()
        return rc

    def create_lug_picker_association(self, lug=None, picker=None, contribution=1):
        if not lug:
            lug = self.create_lug()
        if not picker:
            picker = self.create_picker()
        lpa = LugPicker(lug=lug, picker=picker, contribution=contribution)
        db_session.add(lpa)
        db_session.commit()
        return lpa


class LugTestCase(BaseModelsTestCase):
    def setUp(self):
        BaseModelsTestCase.setUp(self)
        self.l = self.create_lug()

    def test_create_lug(self):
        self.assertTrue(Lug.query.get(1))

    def test_block_relationship(self):
        self.assertTrue(Lug.query.get(1).block)

    def test_orchard_load_relationship(self):
        self.assertTrue(Lug.query.get(1).orchard_load)

    def test_farm_load_relationship(self):
        self.assertTrue(Lug.query.get(1).farm_load)

    def test_lug_picker_associations_relationship(self):
        self.assertTrue(Lug.query.get(1).lug_picker_associations)

class PickerTestCase(BaseModelsTestCase):
    def setUp(self):
        BaseModelsTestCase.setUp(self)
        self.p = self.create_picker()

    def test_create_picker(self):
        self.assertTrue(Picker.query.get(1))

    def test_current_cards_relationship(self):
        self.create_rfid_card(current_picker=self.p)
        self.assertTrue(Picker.query.get(1).current_cards)

class BlockTestCase(BaseModelsTestCase):
    def test_create_block(self):
        self.create_block()
        self.assertTrue(Block.query.get(1))

class OrchardLoadTestCase(BaseModelsTestCase):
    def test_create_orchard_load(self):
        self.create_orchard_load()
        self.assertTrue(OrchardLoad.query.get(1))

class FarmLoadTestCase(BaseModelsTestCase):
    def test_create_farm_load(self):
        self.create_farm_load()
        self.assertTrue(FarmLoad.query.get(1))

class RFIDCardTestCase(BaseModelsTestCase):
    def test_create_rfid_card(self):
        self.create_rfid_card()
        self.assertTrue(Tag.query.get('1'))