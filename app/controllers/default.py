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
from flask_googlemaps import GoogleMaps, Map
import requests

from flask import json

from json import JSONDecoder, JSONDecodeError, JSONEncoder


@lm.user_loader
def load_user(id):
    return session.query(User).filter_by(id=id).first()


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/mapa")
def mapa():
    # creating a map in the view

    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=januária&key=AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y"
                            )
    x = json.loads(response.text)

    #return str(x['results[0].geometry[0].location.lat[0]'])
    a = {
        "results": [
            {
                "address_components": [
                    {
                        "long_name": "1600",
                        "short_name": "1600",
                        "types": ["street_number"]
                    },
                    {
                        "long_name": "Amphitheatre Parkway",
                        "short_name": "Amphitheatre Pkwy",
                        "types": ["route"]
                    },
                    {
                        "long_name": "Mountain View",
                        "short_name": "Mountain View",
                        "types": ["locality", "political"]
                    },
                    {
                        "long_name": "Santa Clara County",
                        "short_name": "Santa Clara County",
                        "types": ["administrative_area_level_2", "political"]
                    },
                    {
                        "long_name": "California",
                        "short_name": "CA",
                        "types": ["administrative_area_level_1", "political"]
                    },
                    {
                        "long_name": "Estados Unidos",
                        "short_name": "US",
                        "types": ["country", "political"]
                    },
                    {
                        "long_name": "94043",
                        "short_name": "94043",
                        "types": ["postal_code"]
                    }
                ],
                "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, EUA",
                "geometry": {
                    "location": {
                        "lat": 37.4215421,
                        "lng": -122.0840106
                    },
                    "location_type": "ROOFTOP",
                    "viewport": {
                        "northeast": {
                            "lat": 37.42289108029149,
                            "lng": -122.0826616197085
                        },
                        "southwest": {
                            "lat": 37.42019311970849,
                            "lng": -122.0853595802915
                        }
                    }
                },
                "place_id": "ChIJ2eUgeAK6j4ARbn5u_wAGqWA",
                "types": ["street_address"]
            }
        ],
        "status": "OK"
    }



    return str(a['location[0].lat[0]'])

    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "<b>Hello World from other place</b>"
            }
        ]
    )
    return render_template('mapa.html', mymap=mymap, sndmap=sndmap)


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


@app.route("/republica/cadastro", methods=["GET", "POST"])
@login_required
def create():
    forme = Home()

    if forme.validate_on_submit():
        try:
            i = ControlHomes()
            i.addHome(int(current_user.get_id()), forme.title.data, forme.value.data, forme.description.data, forme.telephone.data,
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


@app.route("/republica/remove/<int:id>", methods=["GET", "POST"])
def rm(id):
    m = ControlHomes()
    n = session.query(Homes).filter_by(
        id=id).first()
    m.remHome(n)
    return redirect('/republica/meusanuncios')


@app.route("/republica/meusanuncios", methods=["GET", "POST"])
def meusanuncios():
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
