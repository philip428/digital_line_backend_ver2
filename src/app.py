from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config.from_pyfile('dev_config.py')

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

import endpoints.clients_endpoints
import endpoints.lines_endpoints
import endpoints.clerks_endpoints

#import endpoints.test
