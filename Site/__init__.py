from flask import Flask
from flask_restful import Api
from requests import Session

app = Flask(__name__)
api = Api(app)
session = Session()

