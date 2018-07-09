from app import app
from flask import render_template
from datetime import datetime
from app.models.forms import LoginForm
from app.models.tables import User, Homes
from app.controllers.functions import ControlHomes
from app import db,session,Session

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            session.add(User(form.username.data, form.password.data, form.username.data, form.username.data))
            session.commit()        
            return "OK"
        except:
            session.rollback()
            return "OPS"
            
        finally:
            session.close()        
    else:
        print(form.errors)
    return render_template('login.html',
                                    form=form
                                    )

@app.route("/republica/cadastro")
def create():
    form = LoginForm()
    return render_template('create.html', form=form)
   # i = ControlHomes()  
  #  i.addHome(1,"gui", 23.23, "OLA", "1111111111", datetime.now(),"39480000", "SS","sdff", 2, "CASA")
   # k = ControlHomes()
  #  j = k.listHomes()
  #  for l in j:
   #     return (l)
    
   