from CherryHarvestAPI import models
from CherryHarvestAPI.authorisation import auth
from CherryHarvestAPI.database import db_session
from CherryHarvestAPI.resources.common import block_fields
from flask.ext.restful import Resource, marshal_with, reqparse, abort
from sqlalchemy.exc import IntegrityError


def orientation(value):
    if value not in models.Block.ORIENTATIONS:
        raise ValueError('{} is not a valid orientation')
    return value

block_parser = reqparse.RequestParser()
block_parser.add_argument('id', type=int)
block_parser.add_argument('variety', required=True)
block_parser.add_argument('orientation', type=orientation)
block_parser.add_argument('plant_year', type=int)


class Blocks(Resource):
    @marshal_with(block_fields)
    def get(self):
        blocks = models.Block.query.all()
        print blocks
        return blocks

    @auth.login_required
    @marshal_with(block_fields)
    def post(self):
        args = block_parser.parse_args()
        block = models.Block(**args)
        try:
            db_session.add(block)
            db_session.commit()
        except IntegrityError, e:
            db_session.rollback()
            return {'error' : e.message}, 409
        return block
    
class Block(Resource):
    @marshal_with(block_fields)
    def get(self, id):
        block = models.Block.query.get(id)
        if not block:
            return abort(404)
        return block

    @auth.login_required
    @marshal_with(block_fields)
    def patch(self, id):
        args = block_parser.parse_args()
        block = models.Block.query.get(id)
        if not block:
            return abort(404)
        for attr, value in args.items():
            if value:
                setattr(block, attr, value)
        db_session.commit()
        return block

    @auth.login_required
    @marshal_with(block_fields)
    def put(self, id):
        args = block_parser.parse_args()
        block = models.Block.query.get(id)
        if not block:
            return abort(404)
        for attr, value in args.items():
            setattr(block, attr, value)
        db_session.commit()
        return block

    @auth.login_required
    def delete(self, id):
        block = models.Block.query.get(id)
        if not block:
            return abort(404)
        db_session.delete(block)
        db_session.commit()
        return '', 204