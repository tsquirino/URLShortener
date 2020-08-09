from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flasgger import Swagger

from db import db
from models import delete_expired
import routes

# Creating web application
application = Flask(__name__)
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configurating database
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url.db'
db.init_app(application)

# Swagger API documentation
swagger_template = {
    "info": {
        "title": "URLShortener",
        "description": "API for generating short URLs."
    }
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(application, template=swagger_template, config=swagger_config)


# Creating endpoints
@application.route('/<code>', methods=['GET'])
def redirect_code(code):
    """Endpoint for redirecting to original URL from a short URL.
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: true
        description: Short URL code
    responses:
      200:
        description: Successful request. Redirects user to the original URL corresponding to the given code.
      404:
        description: Unsuccessful request. Given code is not associated in the database with an URL.
    """
    return routes.redirect_code(code)


@application.route('/new', methods=['POST'])
def new():
    """Endpoint for creating a new URL entry in database.
    ---
    parameters:
      - name: shortened_url
        in: formData
        type: string
        required: false
        description: Desired short URL code (if not given, a random 5-character string will be generated)
      - name: original_url
        in: formData
        type: string
        required: true
        description: Original URL for redirection
      - name: expiration_date
        in: formData
        type: string
        required: false
        description: Expiration date for the URL to be generated in '%Y-%m-%d' format, e.g. 2020-12-31 (if not given,
                        URL will be set to expire in 7 days)
    responses:
      200:
        description: Successful request. Returns JSON string with the generated URL and the newly added database entry.
      404:
        description: Unsuccessful request. Returns JSON string with error message.
    """
    return routes.new()


@application.route('/login', methods=['GET', 'POST'])
def login():
    return routes.login()


@application.route('/logout', methods=['GET'])
def logout():
    return routes.logout()


@application.route('/', methods=['GET'])
def home():
    return routes.home()


# Schedule for cleaning expired entries from database every hour
with application.app_context():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=lambda: delete_expired(application), trigger="interval", hours=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

# Run application
if __name__ == '__main__':
    application.run()
