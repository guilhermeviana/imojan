from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from app import Base, db


class User(Base):
    __tablename__ = "users"

    id  = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    passwords = Column(String(50))
    nome = Column(String(50))
    email = Column(String(50), unique=True)


    def __init__(self, username=None, password=None, name=None, email=None):
        self.username = username
        self.passwords = password
        self.nome = name
        self.email = email


    def __repr__(self):
        return "<User %r>" % self.username


##Criar endereço de um imóvel
#class Address(object):
  ##  zipCode = Column(String(8))
   ## street = Column (String(200))
  ##  neighborhood = Column(String(200))
  ##  number = Column(Integer)
   ## complement = Column (String(100))

  ##  def __init__(self,zipCode,street, neighborhood, number,complement):
       ## self.zipCode = zipCode
      ##  self.street = street
      ##  self.neighborhood = neighborhood
      ##  self.number = number
      ##  self.complement = complement

##Criar "anuncio", contendo suas informações
##Obs: o atributo address precisa ser preenchido atraves do método addAddress
class Homes(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True)    
    client_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200))
    value = Column(Float)
    description = Column(Text)
    telephone = Column (String()) 
    publicationDate = Column(DateTime,default=datetime.now)
    zipCode = Column(String(8))
    street = Column (String(200))
    neighborhood = Column(String(200))
    number = Column(Integer)
    complement = Column (String(100))



  ##  def addAdrress(self, zipCode,street,neighborhood,number,complement):
      ##  self.address.zipCode = zipCode
      ##  self.address.street = street
     ##   self.address.neighborhood = neighborhood
     ##   self.address.number = number
      ##  self.address.complement = complement

    def __init__(self, client_id,title,value,description,telephone,publicationDate,zipCode,street, neighborhood, number,complement):
        self.client_id = client_id
        self.title = title
        self.value = value
        self.description = description
        self.telephone = telephone
        self.publicationDate = publicationDate
        self.zipCode = zipCode
        self.street = street
        self.neighborhood = neighborhood
        self.number = number
        self.complement = complement

    def __repr__(self):
        return '<Home: title{0}>'.format(self.title)