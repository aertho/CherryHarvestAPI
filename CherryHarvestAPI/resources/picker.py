from CherryHarvestAPI import models, app
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
import regex

picker_fields = {
    'id' : fields.Integer,
    'first_name' : fields.String,
    'last_name' : fields.String,
    'pay_rate' : fields.Float,
    'pay_type' : fields.String,
    'mobile_number' : fields.String,
    'email' : fields.String,
    'today_total' : fields.Float,
    'href' : fields.Url('picker',  absolute=True, scheme=app.config["SCHEME"])
}

def pay_type(value):
    if value not in models.Picker.PAY_TYPES:
        raise ValueError("{} is not a valid pay type".format(value))
    return value

def mobile_number(value):
    if not regex.match(r'/^(\+\d{1,3}[- ]?)?\d{10}$/', value):
        raise ValueError("{} is not a valid mobile number".format(value))
    return value

def email(value):
    if not regex.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'):
        raise ValueError("{} is not a valid email".format(value))
    return value

picker_parser = reqparse.RequestParser()
picker_parser.add_argument('id', type=int)
picker_parser.add_argument('first_name', required=True)
picker_parser.add_argument('last_name')
picker_parser.add_argument('pay_rate', type=float)
picker_parser.add_argument('pay_type', type=pay_type)
picker_parser.add_argument('mobile_number', type=mobile_number)
picker_parser.add_argument('email', type=email)

class Pickers(Resource):
    @marshal_with(picker_fields)
    def get(self):
        pickers = models.Picker.query.all()
        return pickers

    @auth.login_required
    @marshal_with(picker_fields)
    def post(self):
        args = picker_parser.parse_args()
        picker = models.Picker(**args)
        try:
            db_session.add(picker)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return {'error' : e.message}, 409
        return picker
    
class Picker(Resource):
    @marshal_with(picker_fields)
    def get(self, id):
        picker = models.Picker.query.get(id)
        if not picker:
            return abort(404)
        return picker

    @auth.login_required
    @marshal_with(picker_fields)
    def patch(self, id):
        args = picker_parser.parse_args()
        picker = models.Picker.query.get(id)
        if not picker:
            return abort(404)
        for attr, value in args.items():
            if value:
                setattr(picker, attr, value)
        db_session.commit()
        return picker

    @auth.login_required
    @marshal_with(picker_fields)
    def put(self, id):
        args = picker_parser.parse_args()
        picker = models.Picker.query.get(id)
        if not picker:
            return abort(404)
        for attr, value in args.items():
            setattr(picker, attr, value)
        db_session.commit()
        return picker

    @auth.login_required
    def delete(self, id):
        picker = models.Picker.query.get(id)
        if not picker:
            return abort(404)
        db_session.delete(picker)
        db_session.commit()
        return '', 204