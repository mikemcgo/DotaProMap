from flask import *
from pymongo import MongoClient

# Not sure if these imports are needed
from bson import Binary, Code
from bson.json_util import dumps

db_client = MongoClient()
db = db_client.dota

player_data = Blueprint('player_data', __name__, template_folder='templates')

@player_data.route('/api/v1/player_data/<id>')
def player_data_api_v1(id):
	return dumps(db.players.find_one({"id": id}))
