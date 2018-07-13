from app import app
from flask import render_template, flash, redirect, request, jsonify, json
from datetime import datetime
from app.models.forms import LoginForm, Home
from app.models.tables import User, Homes
from app.controllers.functions import ControlHomes
from app import db, session, Session
from app.templates.cep import ListCep
import pycep_correios
from flask_login import login_user, logout_user, login_required, current_user
from app import lm
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps, Map, googlemap
import requests



import googlemaps

from flask import json

from json import JSONDecoder, JSONDecodeError, JSONEncoder



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

# blueprint

@app.route("/t",methods=["GET", "POST"])
def aa():
    return render_template('teste.html')

@app.route("/republica/cadastro", methods=["GET", "POST"])
#@login_required
def create():
    if current_user.get_id()==None:
        return redirect('/login')
    forme = Home()
    if forme.validate_on_submit():
        try:
            maps = googlemaps.Client(key='AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y')
            h = maps.geocode("Rua "+forme.street.data+" "+forme.neighborhood.data+" "+str(forme.number.data)+" "+forme.zipCode.data)    
            lat = str(h[0]['geometry']['location']['lat'])
            lng = str(h[0]['geometry']['location']['lng'])

            i = ControlHomes()
            i.addHome(int(current_user.get_id()), forme.title.data, forme.value.data, forme.description.data, forme.telephone.data,
                      datetime.now(), forme.zipCode.data, forme.street.data, forme.neighborhood.data, forme.number.data, forme.complement.data,lat,lng)
            flash("Anúncio cadastrado!")
            return redirect('/republica/meusanuncios')
        except:
            return render_template('create.html', forme=forme)
        finally:
            session.close()
    else:
        return render_template('create.html', forme=forme)
    return render_template('create.html', forme=forme)




@app.route("/republica/remove/<int:id>", methods=["GET", "POST"])
def rm(id):
    m = ControlHomes()
    n = session.query(Homes).filter_by(
        id=id).first()
    m.remHome(n)
    return redirect('/republica/meusanuncios')


@app.route("/republica/meusanuncios", methods=["GET", "POST"])
def meusanuncios():
    if current_user.get_id()==None:
        return redirect('/login')
    user = session.query(Homes).filter_by(
        client_id=current_user.get_id()).all()
    return render_template('meusanuncios.html', user=user)


@app.route("/get", methods=["POST", "GET"])
def liste():
    user = session.query(User).all()
    for p in user:
        print(p.email)


@app.route("/cep", methods=["POST", "GET"])
def listy():
    n = ListCep()
    return str(n.loadCep('04880090'))





@app.route("/republica/localizar")
def mapa():
    #response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=42.1282269,-87.7108162&key=AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y"
             #               )
   # x = json.loads(response.content)
    alls = session.query(Homes).order_by().all()
    #return str (alls[2].lat)
    maps = googlemaps.Client(key='AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y')
    markerso= []

    for i in alls:
       # h = maps.geocode("Rua "+str(i.lat)+" "+str(i.lng))
        #lat = str(h[0]['geometry']['location']['lat'])
        #lgn = str(h[0]['geometry']['location']['lng'])
        markerso.append({'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': i.lat, 'lng': i.lng, 'infobox': str(i.title+" "+str(i.value)) })
        lat = i.lat
        lng = i.lng


    mymap = Map(
        maptype="ROADMAP",
        style=" #sndmap { height:800px!important;width:100%!important;margin:0; }",
        identifier="view-side",
        zoom=1,
        lat=-14.235004,
        lng=-51.92528,
        markers=[(-14.235004, -51.92528)],
        fit_markers_to_bounds = True,
        region='Brazil',
        language='pt-br'
        
    
    )


    sndmap = Map(
        identifier="sndmap",
        zoom=8,
        lat=-14.235004,
        lng=-51.92528,
        markers= markerso,
        fit_markers_to_bounds = True,
       
    )


    
   # https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

    return render_template('mapa.html', mymap=mymap, sndmap=sndmap,markerso=markerso)
    
