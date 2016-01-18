from CherryHarvestAPI import models
from CherryHarvestAPI.resources.common import lug_picker_fields
from flask.ext.restful import Resource, marshal_with


class LugPickers(Resource):
    @marshal_with(lug_picker_fields)
    def get(self):
        lug_pickers = models.LugPicker.query.all()
        return lug_pickers