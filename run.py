
from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from sqlalchemy.sql.functions import current_user

from config import config_dict
from app import create_app, db
from app import extensions

from flask_apscheduler import APScheduler

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# The configuration

# for production:
# get_config_mode = 'Production'
# for testing:
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config )
scheduler = APScheduler()
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )


def configure_celery(app):

    extensions.celery.conf.update(
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        broker_url=app.config['CELERY_BROKER_URL']
    )

    return extensions.celery

celery = configure_celery(app)
app.app_context().push()

from app.home.automatic_tasks import *

if __name__ == "__main__":
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", minutes=5)
    scheduler.add_job(id = 'Update Influencers', func=update_influencers, trigger="interval", days=1)
    scheduler.start()
    app.run(host="0.0.0.0", port="5000", use_reloader=False)
