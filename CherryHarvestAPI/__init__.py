from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)

app.config.from_object('config')
api = Api(app)

from CherryHarvestAPI.resources import api_root, lug, picker,block, orchard_load, farm_load, tag, picker_number, day, season

api.add_resource(api_root.APIRoot, '/', endpoint='api_root')
api.add_resource(lug.Lugs, '/lugs/', endpoint='lugs')
api.add_resource(lug.Lug, '/lugs/<int:id>/', endpoint='lug')
api.add_resource(lug.LugPickers, '/lugs/<int:id>/lug-pickers/', endpoint='lug_pickers')

api.add_resource(picker.Pickers, '/pickers/', endpoint='pickers')
api.add_resource(picker.Picker, '/pickers/<int:id>/', endpoint='picker')

api.add_resource(block.Blocks, '/blocks/', endpoint='blocks')
api.add_resource(block.Block, '/blocks/<int:id>/', endpoint='block')

api.add_resource(orchard_load.OrchardLoads, '/orchard-loads/', endpoint='orchard_loads')
api.add_resource(orchard_load.OrchardLoad, '/orchard-loads/<int:id>/', endpoint='orchard_load')
api.add_resource(orchard_load.OrchardLoadLugs, '/orchard-loads/<int:id>/lugs/', endpoint='orchard_load_lugs')

api.add_resource(farm_load.FarmLoads, '/farm-loads/', endpoint='farm_loads')
api.add_resource(farm_load.FarmLoad, '/farm-loads/<int:id>/', endpoint='farm_load')
api.add_resource(farm_load.FarmLoadLugs, '/farm-loads/<int:id>/lugs/', endpoint='farm_load_lugs')

api.add_resource(tag.Tags, '/tags/', endpoint='tags')
api.add_resource(tag.Tag, '/tags/<epc>/', endpoint='tag')

api.add_resource(picker_number.PickerNumbers, '/picker-numbers/', endpoint='picker_numbers')
api.add_resource(picker_number.PickerNumber, '/picker-numbers/<int:id>/', endpoint='picker_number')

api.add_resource(day.Days, '/days/', endpoint='days')
api.add_resource(day.Day, '/days/<date>/', endpoint='day')
api.add_resource(day.Today, '/today/', endpoint='today')
api.add_resource(day.Yesterday, '/yesterday/', endpoint='yesterday')

api.add_resource(season.Seasons, '/seasons/', endpoint='seasons')
api.add_resource(season.Season, '/seasons/<int:year>/', endpoint='season')
api.add_resource(season.CurrentSeason, '/current-season/', endpoint='current_season')


