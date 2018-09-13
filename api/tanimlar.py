from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Ortamlar, Sureler, Kurumlar,Dayanaklar, PaylasimAmaclari, PaylasimSekilleri, Ulkeler, TanimlarID, getModel

class Tanimlar():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = modelClass   # !!!modelClass() parentezle yaparsan class create edilir, bu koşulda olmaz...

        def __del__(self):
                self.session.close()

        def get(self):
                try:
                        dict = []

                        if (self.model == Sistemler):
                                data = self.session.query(self.model.pidm, self.model.name, self.model.type, self.model.timestamp)
                        elif (self.model == Ulkeler):
                                data = self.session.query(self.model.pidm, self.model.name, self.model.phone_area,self.model.secure, self.model.timestamp)
                        else:
                                data = self.session.query(self.model.pidm, self.model.name, self.model.timestamp)

                        data = data.order_by(self.model.name)

                        for row in data:

                                if (self.model == Sistemler):
                                        dict.append({'pidm':row.pidm, 'name':row.name,'type':row.type, 'timestamp':row.timestamp})
                                elif (self.model == Ulkeler):
                                        dict.append({'pidm':row.pidm, 'name':row.name,'phone_area':row.phone_area,'secure':row.secure, 'timestamp':row.timestamp})
                                else:
                                        dict.append({'pidm':row.pidm, 'name':row.name,'timestamp':row.timestamp})

                        # _json = jsonify({"Tanimlar":dict})
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response("NO DATA found!")
                        else:
                                return _json

                except Exception as e:
                        return Response("sa query error! ",e)

        def add(self):
                        self.session.add(self.model)
                        self.session.commit()
                        print("Add Successfully")
                        return '',204

                        # Add delete için response gerekmediğinden: The HTTP 204: No Content success status response code indicates that the request has succeeded, but that the client doesn't need to go away from its current page. A 204 response is cacheable by default. An ETag header is included in such a response

        def delete(self):
                try:
                        _pidm = int(self.model.pidm)
                        row = self.session.query(Profiller).filter_by(pidm=_pidm).one()
                        self.session.delete(row)
                        self.session.commit()
                        print(row.name+" deleted successfully")
                        return '',204
                except:
                        print("Unknown error on deleting ")
                        return '',404


# def addTanim(modelClass):
#         cc=Tanimlar(modelClass) # create class
#         return cc.add()



def getTanim(id):
    model = getModel(id)
    cc = Tanimlar(model)
    return cc.get()


def addTanim(form):
    _id = form.get('id')
    _name = form.get('name')
    # Güvenli Ülkeler
    _phone_area = form.get('phone_area')
    _secure = form.get('secure')

    model = getModel(_id)
    if (_id==TanimlarID.GuvenliUlkeler):
       cc=Tanimlar(model(name=_name, phone_area=_phone_area, secure=_secure))
    else:
       cc=Tanimlar(model(name=_name))

    return cc.add()

def delTanim(form):
    _id = form.get('id')
    _pidm = form.get('pidm')

    model = getModel(_id)
    cc=Tanimlar(model(pidm=_pidm)) # create class
    return cc.delete()


# if __name__ == "__main__":
#     e = SetProfiller()
#     e.add()

#     print("Successfully..")