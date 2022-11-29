from flask import Flask
from flask_restful import Api
from requests import Session
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
session = Session()
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

