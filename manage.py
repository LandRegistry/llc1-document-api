from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from llc1_document_api.extensions import db
from llc1_document_api.main import app

import os

migrate = Migrate(app, db)

manager = Manager(app)

# ***** For Alembic start ******
manager.add_command('db', MigrateCommand)
# ***** For Alembic end ******


@manager.command
def runserver(port=9999):
    """Run the app using flask server"""

    os.environ["PYTHONUNBUFFERED"] = "yes"
    os.environ["FLASK_LOG_LEVEL"] = "DEBUG"
    os.environ["COMMIT"] = "LOCAL"
    os.environ["APP_NAME"] = "llc1-document-api"

    app.run(debug=True, port=int(port))


if __name__ == "__main__":
    manager.run()
