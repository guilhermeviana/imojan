from app import app
from flask import render_template


from app.models.forms import LoginForm

from app.models.tables import User

from app import db,session

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
    else:
        print(form.errors)
    return render_template('login.html',
                                    form=form
                                    )

@app.route("/teste")
def teste():
   # i = User ("Gui", "123", "glva", "gui@gmail.com" )

    try:
        session.add(User("sss", 123, "ss", "sss"))
        session.commit()
        session.close()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    return "OK";