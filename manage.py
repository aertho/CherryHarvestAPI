from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from CherryHarvestAPI import app
from CherryHarvestAPI.database import Base as db
app.config.from_object('config')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()