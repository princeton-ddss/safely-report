from flask import Flask, session
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from safely_report.survey.form_generator import SurveyFormGenerator
from safely_report.survey.survey_processor import SurveyProcessor

# Create and configure app
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Set up use of server-side sessions
Session(app)

# Set up database
db = SQLAlchemy(app)
Migrate(app, db)

# Construct survey processor and form generator
path_to_xlsform = app.config["XLSFORM_PATH"]
survey_processor = SurveyProcessor(path_to_xlsform, session)
form_generator = SurveyFormGenerator(survey_processor)

from safely_report.survey.views import survey_blueprint  # noqa

# Register routes (i.e., "views")
app.register_blueprint(survey_blueprint, url_prefix="/survey")
