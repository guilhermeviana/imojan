from app.models.tables import User, Homes
from datetime import datetime
from app import session


class ControlHomes(object):

    def __init__(self):
        self.__status = True
    
    def addHome(self, client_id,title,value,description,telephone,publicationDate,zipCode,street, neighborhood, number,complementf):
        try:
            h = Homes(client_id,title,value,description,telephone,publicationDate,zipCode,street, neighborhood, number,complementf)
            session.add(h)
            session.commit()
        except:
            session.rollback()

##Ver com mais calma
    def listHomes(self):
        try:              
            return Homes.query.all()
        except:
            return "OPS"