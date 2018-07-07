from app import db

from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import Base

class User(Base):
    __tablename__ = "users"

    id  = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    passwords = Column(String(50))
    nome = Column(String(50))
    email = Column(String(50), unique=True)


    def __init__(self, username, password, name, email):
        self.username = username
        self.passwords = password
        self.nome = name
        self.email = email

    def __repr__(self):
        return "<User %r>" % self.username

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))


    user = relationship ('User', foreign_keys=user_id)

    def __init__(self, content,user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return "<Post %r>" % self.id

class Follow(Base):
    __tablename__ = "follow"

    id  = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    follow_id = Column(Integer, ForeignKey('users.id'))

    user = relationship ('User', foreign_keys=user_id)
    follower = relationship ('User', foreign_keys=follow_id)
