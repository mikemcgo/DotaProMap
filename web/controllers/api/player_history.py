from flask import *
from pymongo import MongoClient

db_client = MongoClient()
db = db_client.dota

player_history = Blueprint('player_history', __name__, template_folder='templates')

@player_history.route('/api/v1/player_history/<id>')
def player_history_api_v1(id):
	query = db.player.find_one({"id": id})
	print(query[0])
	return str(id)
