from flask import Flask

from pymongo import MongoClient
from flask_restful import Api

app = Flask(__name__)
app.config["SECRET_KEY"] = '47210838d5fc13b84abfc83h6c06b1cde2ac2516'
api = Api(app)

db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['web-gallery']
