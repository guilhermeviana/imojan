from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import login_user

app = Flask(__name__)
app.config.from_object('config')

app.debug = True


engine = create_engine('mysql+pymysql://root:@localhost/python', echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)


from app.models import tables, forms
from app.controllers import default
