from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



app = Flask(__name__)
app.config.from_object('config')

app.debug = True


engine = create_engine('mysql+pymysql://root:@localhost/python', echo=False)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

db = SQLAlchemy(app)



from app.models import tables, forms
from app.controllers import default