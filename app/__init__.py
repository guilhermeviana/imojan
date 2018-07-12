from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import login_user
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.config.from_object('config')

app.debug = True

app.config['GOOGLEMAPS_KEY'] = "AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y"
# Initialize the extension


# you can also pass the key here if you prefer
GoogleMaps(app, key="AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y")



engine = create_engine('mysql+pymysql://root:@localhost/python', echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)


from app.models import tables, forms
from app.controllers import default
