from flask import Flask
import controllers
import config 

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
app.register_blueprint(controllers.main)
app.register_blueprint(controllers.dotamap)

# Register API
app.register_blueprint(controllers.api.player_data)

# Listen on external IPs using the configured port
if __name__ == '__main__':
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
