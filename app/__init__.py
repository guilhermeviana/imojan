from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




app = Flask(__name__)
#app.config.from_object('config')


db = SQLAlchemy(app)


engine = create_engine('mysql://root:@localhost/python')

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()


migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.models import tables, forms
from app.controllers import default
