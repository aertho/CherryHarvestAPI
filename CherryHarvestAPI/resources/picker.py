import datetime

from CherryHarvestAPI import models, app
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from dateutil import parser
from flask import request, url_for
from flask.ext.restful import Resource, marshal_with, reqparse, fields, abort
from sqlalchemy.exc import IntegrityError
import regex

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
picker_parser.add_argument('first_name')
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
        picker = models.Picker(first_name=args['first_name'], last_name=args['last_name'])
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


ranked_picker_fields = {
    'rank' : fields.Integer,
    'total' : fields.Integer,
    'picker' : fields.Nested(picker_fields)
}


def ranked_pickers(picker_function, max_people=10):
    return [
               {'rank' : i,
                'total' : picker_function(p),
                'picker' : p}
                for i, p in enumerate(sorted(models.Picker.query.all(), key= picker_function, reverse=True), 1)
                if picker_function(p) and not p.is_manager][:max_people]

class Leaderboards(Resource):
    def get(self):
        return {
            'daily' : url_for('daily_leaderboard', _external=True, _scheme=app.config["SCHEME"]),
            'weekly' : url_for('weekly_leaderboard', _external=True, _scheme=app.config["SCHEME"]),
            'seasonal' : url_for('seasonal_leaderboard', _external=True, _scheme=app.config["SCHEME"]),
            'all_time' : url_for('all_time_leaderboard', _external=True, _scheme=app.config["SCHEME"]),
        }

class Leaderboard(Resource):
    picker_function = models.Picker.total
    @marshal_with(ranked_picker_fields)
    def get(self):
        if 'date' in request.args:
            try:
                date = parser.parse(request.args['date']).date()
            except ValueError:
                date = datetime.date.today()
        else:
            date = datetime.date.today()
        return ranked_pickers(lambda p: self.picker_function(p, date=date))


class DailyLeaderboard(Leaderboard):
    picker_function = models.Picker.total


class WeeklyLeaderboard(Leaderboard):
    picker_function = models.Picker.weekly_total


class SeasonalLeaderboard(Leaderboard):
    picker_function = models.Picker.seasonal_total


class AllTimeLeaderboard(Leaderboard):
    picker_function = models.Picker.all_time_total