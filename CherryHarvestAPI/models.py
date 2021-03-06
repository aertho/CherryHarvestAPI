import datetime

import pytz
from CherryHarvestAPI.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, BigInteger, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash


class Picker(Base):
    __tablename__ = 'picker'

    PAY_TYPES = ['time','weight']

    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    pay_rate = Column(Float)
    pay_type = Column(String(16))
    mobile_number = Column(String(16))
    email = Column(String(64))
    is_manager = Column(Boolean, default=False, nullable=True)

    picker_lugs = relationship("LugPicker", backref=backref("picker"))

    @property
    def today_total(self):
        return self.total(datetime.date.today())

    @property
    def current_week_total(self):
        return self.weekly_total()

    @property
    def card_count(self):
        return sum([len(pn.current_cards) for pn in self.picker_numbers])

    @property
    def current_season_total(self):
        return self.seasonal_total()

    def seasonal_total(self, date=None):
        if not date:
            date = datetime.date.today()
        return self.total(datetime.date(date.year, 1, 1), date)

    def weekly_total(self, date=None):
        if date is None:
            date = datetime.date.today()
        return self.total(date - datetime.timedelta(days=date.isoweekday()-1), date)

    def all_time_total(self, *args, **kwargs):
        return self.total()

    def total(self, date=None, to_date=None):
        if date and to_date:
            return sum([lp.contribution * lp.lug.weight for lp in self.picker_lugs if
                        lp.lug.orchard_load.arrival_time.date() >= date and lp.lug.orchard_load.arrival_time.date() <=
                        to_date])
        if date:
            return sum([lp.contribution*lp.lug.weight for lp in self.picker_lugs if lp.lug.orchard_load.arrival_time.date() == date])
        return sum(lp.contribution*lp.lug.weight for lp in self.picker_lugs)



class Block(Base):
    __tablename__ = 'block'
    ORIENTATIONS = ['north', 'west']
    id = Column(Integer, primary_key=True)
    variety = Column(String)
    plant_year = Column(Integer)
    orientation = Column(String(16))

    @property
    def today_total(self):
        return self.daily_total()

    def daily_total(self, date=None):
        if date is None:
            date = datetime.date.today()
        return sum([l.weight for l in self.lugs if l.orchard_load.arrival_time.date() == date])

    @property
    def current_season_total(self):
        return self.seasonal_total()

    def seasonal_total(self, date=None, year=None):
        if year:
            date = datetime.date(year, 12, 31)
        if date is None:
            date = datetime.date.today()
        return self.total(datetime.date(date.year, 1, 1), date)

    def weekly_total(self, date=None):
        if date is None:
            date = datetime.date.today()
        return self.total(date - datetime.timedelta(days=date.isoweekday()-1), date)

    def all_time_total(self, *args, **kwargs):
        return self.total()

    def total(self, date=None, to_date=None):
        if date and to_date:
            return sum([l.weight for l in self.lugs if
                        l.orchard_load.arrival_time.date() >= date and l.orchard_load.arrival_time.date() <=
                        to_date])
        if date:
            return sum([l.weight for l in self.lugs if l.orchard_load.arrival_time.date() == date])
        return sum(l.weight for l in self.lugs)



class Load(Base):
    __tablename__ = 'load'
    id = Column(Integer, primary_key=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    type = Column(String(32))
    lugs = []

    __mapper_args__ = {
        'polymorphic_identity' : 'load',
        'polymorphic_on' : 'type'
    }

    @property
    def total(self):
        return sum([l.weight or 0 for l in self.lugs])

class OrchardLoad(Load):
    __tablename__ = 'orchard_load'
    id = Column(Integer, ForeignKey(Load.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity' : 'orchard_to_fridge_load',
    }

class FarmLoad(Load):
    __tablename__ = 'farm_load'
    id = Column(Integer, ForeignKey(Load.id), primary_key=True)
    destination = Column(String(32))

    __mapper_args__ = {
        'polymorphic_identity' : 'fridge_to_factory_load',
    }

class Lug(Base):
    __tablename__ = 'lug'
    id = Column(Integer, primary_key=True)

    weight = Column(Float)
    current_status = Column(String(16))

    block_id = Column(Integer, ForeignKey(Block.id))
    orchard_load_id = Column(Integer, ForeignKey(OrchardLoad.id))
    farm_load_id = Column(Integer, ForeignKey(FarmLoad.id))

    block = relationship(Block, backref = backref('lugs'))
    orchard_load = relationship(OrchardLoad, backref = backref('lugs'))
    farm_load = relationship(FarmLoad, backref = backref('lugs'))
    pickers = association_proxy('lug_pickers', 'picker')

class LugPicker(Base):
    __tablename__ = 'lug_picker'
    picker_id = Column(Integer, ForeignKey('picker.id'), primary_key=True)
    lug_id = Column(Integer, ForeignKey('lug.id'), primary_key=True)
    contribution = Column(Float) #decimal between 0 and 1

    lug = relationship(Lug, backref = 'lug_pickers')

class PickerNumber(Base):
    __tablename__ = 'picker_number'
    id = Column(Integer, primary_key=True)
    picker_id = Column(Integer, ForeignKey(Picker.id))

    picker = relationship(Picker, backref=backref('picker_numbers'))

    @property
    def card_count(self):
        return len(self.current_cards)


class Tag(Base):
    __tablename__ = 'card'
    epc = Column(String(128), primary_key=True)
    current_picker_number_id = Column(Integer, ForeignKey(PickerNumber.id))
    current_lug_id = Column(Integer, ForeignKey('lug.id'))

    current_picker_number = relationship(PickerNumber, backref=backref('current_cards'))
    current_lug = relationship(Lug)

class User(Base):
    __tablename__ = 'cha_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)