from flask_script import Manager, Server
from app import app
from flask_migrate import Migrate, MigrateCommand
from models import db


manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)
manager.add_command('start', Server(port=8000, use_debugger=True))

if __name__ == '__Main__':
    manager.run()
