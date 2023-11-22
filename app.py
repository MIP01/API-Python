# Importing the necessary modules and libraries
from flask import Flask
from route.myroute import items,sellers
from flask_migrate import Migrate
from model.mymodel import db

app = Flask(__name__)
app.json.sort_keys = False

#Migrate func
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#Regis route
app.register_blueprint(items, url_prefix='/api/items')
app.register_blueprint(sellers, url_prefix='/api/sellers')



if __name__ == '__main__':
    app.debug = True
    app.run()