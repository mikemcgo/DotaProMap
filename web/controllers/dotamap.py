from flask import *

dotamap = Blueprint('dotamap', __name__, template_folder='templates')

@dotamap.route('/dotamap')
def dotamap_route():
	return render_template("dotamap.html")
