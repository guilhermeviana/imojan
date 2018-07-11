from app import app
from flask import render_template, flash, redirect, request
from datetime import datetime
from app.models.forms import LoginForm, Home
from app.models.tables import User, Homes
from app.controllers.functions import ControlHomes
from app import db, session, Session
from app.templates.cep import ListCep
import pycep_correios
from flask_login import login_user, logout_user, login_required,current_user
from app import lm
from flask_login import LoginManager





@lm.user_loader
def load_user(id):
    return session.query(User).filter_by(id=id).first()


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(
            username=form.username.data).first()
        if user and user.passwords == form.passwords.data:
            login_user(user)
            return redirect('/')
        else:
            flash("Usuário ou senha incorreto")
            return render_template('login.html',
                                   form=form
                                   )
    else:
        return render_template('login.html',
                               form=form
                               )
    return redirect('/login')


@app.route("/republica/cadastro", methods=["GET", "POST"])
@login_required
def create():
    forme = Home()
    if forme.validate_on_submit():
        try:           
            i = ControlHomes()
            i.addHome( int (current_user.get_id()), forme.title.data, forme.value.data, forme.description.data, forme.telephone.data,
                      datetime.now(), forme.zipCode.data, forme.street.data, forme.neighborhood.data, forme.number.data, forme.complement.data)
            flash("Anúncio cadastrado!")
            return redirect('/republica/meusanuncios')
        except:
            return render_template('create.html', forme=forme)
        finally:
            session.close()
    else:
        return render_template('create.html', forme=forme)
    return render_template('create.html', forme=forme)

@app.route("/republica/localizar", methods=["GET", "POST"])
def list():
    return "OK"


@app.route("/republica/meusanuncios", methods=["GET", "POST"])
def meusanuncios():
    user = session.query(Homes).filter_by(
            client_id=current_user.get_id()).all()
    return render_template('meusanuncios.html',user=user)


@app.route("/get", methods=["POST", "GET"])
def liste():
    user = session.query(User).all()
    for p in user:
        print(p.email)


@app.route("/cep", methods=["POST", "GET"])
def listy():
    n = ListCep()
    return str(n.loadCep('04880090'))
