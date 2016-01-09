from CherryHarvestAPI import app
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