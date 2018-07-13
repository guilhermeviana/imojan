from app.models.tables import User, Homes
from datetime import datetime
from app import session


class ControlHomes(object):

    def __init__(self):
        self.__status = True

    def addHome(self, client_id, title, value, description, telephone, publicationDate, zipCode, street, neighborhood, number, complementf,lat,lng):
        try:
            h = Homes(client_id, title, value, description, telephone,
                      publicationDate, zipCode, street, neighborhood, number, complementf,lat,lng)
            session.add(h)
            session.commit()
        except:
            session.rollback()

    def remHome(self, Homes):
        session.delete(Homes)
        session.commit()
        session.close()
        


