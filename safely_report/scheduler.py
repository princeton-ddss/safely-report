from time import time

from flask import current_app
from flask_apscheduler import APScheduler
from flask_session import FileSystemSessionInterface

scheduler = APScheduler()


# Add a job to clear any expired sessions every hour
@scheduler.task(trigger="interval", seconds=3600)
def clear_expired_sessions():
    with scheduler.app.app_context():
        interface = scheduler.app.session_interface
        assert isinstance(interface, FileSystemSessionInterface)
        interface.cache._remove_expired(now=time())
        current_app.logger.info("Expired sessions have been cleared")
