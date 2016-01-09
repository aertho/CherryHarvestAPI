from copy import copy

from CherryHarvestAPI import models, app
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources import load
from CherryHarvestAPI.resources.common import simple_lug_fields
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
import regex

_farm_load_fields = copy(load.outer_load_fields)
_farm_load_fields['destination'] = fields.String
# _farm_load_fields['lugs'].endpoint = 'farm_load_lugs'

_farm_load_parser = copy(load.outer_load_parser)
# _farm_load_parser.add_argument('destination')



class FarmLoads(load.Loads):
    farm_load_fields = _farm_load_fields
    farm_load_parser = _farm_load_parser
    
class FarmLoad(load.Load):
    farm_load_fields = _farm_load_fields
    farm_load_parser = _farm_load_parser

class FarmLoadLugs(load.LoadLugs):
    pass