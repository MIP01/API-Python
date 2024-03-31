# Importing the necessary modules and libraries
from flask import Flask
from flask_cors import CORS
from route.myroute import items, sellers, auth
from flask_migrate import Migrate
from model.mymodel import db


app = Flask(__name__)
CORS(app)
app.json.sort_keys = False

#Migrate func
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#Regis route
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(items, url_prefix='/api/items')
app.register_blueprint(sellers, url_prefix='/api/sellers')



if __name__ == '__main__':
    app.debug = True
    app.run()