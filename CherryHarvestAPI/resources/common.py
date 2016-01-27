import datetime

from CherryHarvestAPI import app, models
from flask.ext.restful import fields, marshal
from flask.ext.restful.fields import get_value

class NestedWithEmpty(fields.Nested):
    """
    Allows returning an empty dictionary if marshaled value is None
    """
    def __init__(self, nested, allow_empty=True, **kwargs):
        self.allow_empty = allow_empty
        super(NestedWithEmpty, self).__init__(nested, **kwargs)

    def output(self, key, obj):
        value = get_value(key if self.attribute is None else self.attribute, obj)
        if value is None:
            if self.allow_null:
                return None
            elif self.allow_empty:
                return {}

        return marshal(value, self.nested)


def ranked_pickers(picker_function=None, date=None, max_people=10):
    if not picker_function:
        if not date:
            date = datetime.date.today()
        picker_function = lambda p: models.Picker.total(p, date)
    return [
               {'rank' : i,
                'total' : picker_function(p),
                'picker' : p}
                for i, p in enumerate(sorted(models.Picker.query.all(), key= picker_function, reverse=True), 1)
                if picker_function(p) and not p.is_manager][:max_people]

def totalled_blocks(block_function=None, date=None):
    if not block_function:
        if not date:
            date = datetime.date.today()
        block_function = lambda b: models.Block.total(b, date)
    return [
               {'total' : block_function(b),
                'block' : b}
                for b in sorted(models.Block.query.all(), key= block_function, reverse=True) if block_function(b)]


block_fields = {
    'id' : fields.Integer,
    'variety': fields.String,
    'orientation' : fields.String,
    'plant_year' : fields.Integer,
}
totalled_block_fields = {
    'total' : fields.Integer,
    'block' : fields.Nested(block_fields)
}
orchard_load_fields = {
    'id' : fields.Integer,
    'total' : fields.Integer,
    'departure_time' : fields.DateTime(dt_format='iso8601'),
    'arrival_time' : fields.DateTime(dt_format='iso8601'),
    # 'destination' : fields.String,
    # 'lugs' : fields.Url('load_lugs', absolute=True, scheme=app.config['SCHEME'])
}
lug_fields = {
    'id' : fields.Integer,
    'weight' : fields.String,
    'current_status' : fields.String,
    # 'lug_pickers' : fields.Url('lug_lug_pickers', absolute=True, scheme=app.config["SCHEME"]),
    'block_id' : fields.Integer,
    'block' : NestedWithEmpty({'href' : fields.Url('block', absolute=True, scheme=app.config["SCHEME"])}),
    'orchard_load_id' : fields.Integer,
    'orchard_load' : NestedWithEmpty({'href' : fields.Url('orchard_load', absolute=True, scheme=app.config["SCHEME"])}),
    'farm_load_id' : fields.Integer,
    'farm_load' : NestedWithEmpty({'href' : fields.Url('farm_load', absolute=True, scheme=app.config["SCHEME"])}),
}
lug_picker_fields = {
    'contribution' : fields.Float,
    'picker_id' : fields.Integer,
    'lug_id' : fields.Integer,
    'picker' : NestedWithEmpty({'href' : fields.Url('picker', absolute=True, scheme=app.config["SCHEME"])}),
    'lug' : NestedWithEmpty({'href':fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])}),
}
farm_load_fields = {
    'id' : fields.Integer,
    'net_weight' : fields.Float,
    'departure_time' : fields.DateTime,
    'arrival_time' : fields.DateTime,
    'destination' : fields.String,
    # 'lugs' : fields.Url('load_lugs', absolute=True, scheme=app.config['SCHEME'])
}
picker_fields = {
    'id' : fields.Integer,
    'first_name' : fields.String,
    'last_name' : fields.String,
    # 'pay_rate' : fields.Float,
    # 'pay_type' : fields.String,
    # 'mobile_number' : fields.String,
    # 'email' : fields.String,
    'picker_numbers' : fields.List(fields.Nested({'id':fields.Integer})),
    'card_count' : fields.Integer,
    'href' : fields.Url('picker',  absolute=True, scheme=app.config["SCHEME"])
}
picker_number_fields = {
    'id' : fields.Integer,
    'picker_id' : fields.Integer,
    'picker' : NestedWithEmpty({'href' : fields.Url('picker', absolute=True, scheme=app.config["SCHEME"])}),
    'card_count' : fields.Integer,
}
tag_fields = {
    'epc' : fields.String,
    'current_picker_number_id' : fields.Integer,
    'current_lug_id' : fields.Integer,
    'current_picker_number' : NestedWithEmpty({'href' : fields.Url('picker_number', absolute=True, scheme=app.config["SCHEME"])}),
    'current_lug' : NestedWithEmpty({'href' : fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])})
}
ranked_picker_fields = {
    'rank' : fields.Integer,
    'total' : fields.Integer,
    'picker' : fields.Nested(picker_fields)
}
period_fields = {
    'total' : fields.Integer,
    'totalled_blocks' : fields.Nested(totalled_block_fields),
    'orchard_loads' : fields.Nested(orchard_load_fields),
    'ranked_pickers' : fields.Nested(ranked_picker_fields),
}