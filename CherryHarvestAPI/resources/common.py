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

simple_lug_fields = {
    "href" : fields.Url('lug', absolute=True, scheme=app.config["SCHEME"])
}


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