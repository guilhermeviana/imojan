from app import app
from flask import render_template, flash, redirect, request, jsonify, json
from datetime import datetime
from app.models.forms import LoginForm, Home
from app.models.tables import User, Homes
from app.controllers.functions import ControlHomes
from app import db, session, Session
import pycep_correios
from flask_login import login_user, logout_user, login_required, current_user
from app import lm
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps, Map, googlemap
import requests
import googlemaps
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






@app.route("/republica/cadastro", methods=["GET", "POST"])
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


@app.route("/republica/localizar")
def mapa():
    alls = session.query(Homes).order_by().all()
    maps = googlemaps.Client(key='AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y')
    markerso= []

    for i in alls:
        markerso.append({'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': i.lat, 'lng': i.lng, 'infobox': str("<h5>"+i.title+" </h5>"+"<br> <strong>Valor:</strong> "+str(i.value)+" <br><strong> Contato: </strong>"+str(i.telephone) + "<br> <strong>Descrição: </strong> "+ i.description) })
        lat = i.lat
        lng = i.lng

    mymap = Map(
        maptype="ROADMAP",
        style=" #sndmap { height:800px!important;width:100%!important;margin:0; }",
        identifier="view-side",
        zoom=5,
        lat=-14.235004,
        lng=-51.92528,
        markers=[(-14.235004, -51.92528)],
        fit_markers_to_bounds = True,
        region='Brazil',
        language='pt-br'
    )


    sndmap = Map(
        identifier="sndmap",
        zoom=5,
        lat=-14.235004,
        lng=-51.92528,
        markers= markerso,
        fit_markers_to_bounds = True,
    )
    return render_template('mapa.html', mymap=mymap, sndmap=sndmap,markerso=markerso)
    


###API REST 
@app.route("/republica/get", methods=["GET"])
@app.route("/republica/get/<int:id>", methods=["GET"])
@app.route("/republica/get/<title>", methods=["GET"])
def get(id=None,title=None):
    alls = []
    if not id and not title:
        homes = session.query(Homes).all()
    elif id:
        homes = session.query(Homes).filter_by(
        id=id).all()
    elif title:
        homes = session.query(Homes).filter_by(
        title=title).all()

    for h in homes:
        alls.append({'Titulo': h.title, 'Valor': h.value, 'Descricao': h.description , 
        'Endereco':[{
            'Rua': h.street,
            'Numero': h.number,
            'Complemento': h.complement,
            'Bairro': h.neighborhood,
            'CEP': h.zipCode
        }],
        'Telefone': h.telephone})

    return jsonify({'republicas': alls})


####POST

@app.route("/republica/post",methods=["POST"])
def addPost():
    rep = {'Titulo': request.json['Titulo'], 'Valor': request.json['Valor'], 'Descricao': request.json['Descricao'] , 
        'Endereco':[{
            'Rua': request.json['Endereco'][0]['Rua'],
            'Numero': request.json['Endereco'][0]['Numero'],
            'Complemento': request.json['Endereco'][0]['Complemento'],
            'Bairro': request.json['Endereco'][0]['Bairro'],
            'CEP': request.json['Endereco'][0]['CEP']
        }],
        'Telefone': request.json['Telefone']}
    maps = googlemaps.Client(key='AIzaSyC5t7IJz1xp-3huks0QEOVv5eFOv6Lal4Y')
    l = maps.geocode("Rua "+request.json['Endereco'][0]['Rua']+" "+request.json['Endereco'][0]['Bairro']+" "+str(request.json['Endereco'][0]['Numero'])+" "+request.json['Endereco'][0]['CEP'])    
    l = maps.geocode("RUA G, Jardim Estela, 206 Januária 39480000")

    latt = str(l[0]['geometry']['location']['lat'])
    lngg = str(l[0]['geometry']['location']['lng'])

    current_user.is_autenticate = True
    i = ControlHomes()
    i.addHome(2, request.json['Titulo'], request.json['Valor'], request.json['Descricao'], request.json['Telefone'],
        datetime.now(), request.json['Endereco'][0]['CEP'], request.json['Endereco'][0]['Rua'], request.json['Endereco'][0]['Complemento'], request.json['Endereco'][0]['Numero'], request.json['Endereco'][0]['Complemento'],latt,lngg)

    return  jsonify({'result': rep})


@app.route("/republica/put/<int:id>",methods=["PUT","POST"])
def updatePut(id):
    homes = session.query(Homes).filter_by(
        id=id).first()
    homes.title = request.json['Titulo']
    homes.value = request.json['Valor']
    homes.description = request.json['Descricao']
    homes.telephone = request.json['Telefone']
    homes.zipCode = request.json['Endereco'][0]['CEP']
    homes.street = request.json['Endereco'][0]['Rua']
    homes.neighborhood = request.json['Endereco'][0]['Bairro']
    homes.number = request.json['Endereco'][0]['Numero']
    homes.complement = request.json['Endereco'][0]['Complemento']
    session.commit()
    return redirect('/')


@app.route("/republica/del/<int:id>",methods=["DELETE","GET"])
def delPut(id):
    homes = session.query(Homes).filter_by(
        id=id).first()    
    session.delete(homes)
    try:
        session.commit()
        return jsonify({'status': 'APAGADO'})
    except:
        return jsonify ({'status': 'FALHA'})