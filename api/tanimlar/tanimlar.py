from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Ortamlar, Sureler, Kurumlar, Dayanaklar, PaylasimAmaclari, PaylasimSekilleri, Ulkeler, TanimlarID, getModel
from api.tanimlar.common import str2bool


class Tanimlar():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                # !!!modelClass() parentezle yaparsan class create edilir, bu koşulda olmaz...
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def get(self):
                try:
                        dict = []

                        if (self.model == Sistemler):
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.local, self.model.timestamp)
                        elif (self.model == Ulkeler):
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.phone_area, self.model.secure, self.model.timestamp)
                        else:
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.timestamp)

                        data = data.order_by(self.model.name)

                        for row in data:

                                if (self.model == Sistemler):
                                        dict.append(
                                            {'pidm': row.pidm, 'name': row.name, 'local': row.local, 'timestamp': row.timestamp})
                                elif (self.model == Ulkeler):
                                        dict.append(
                                            {'pidm': row.pidm, 'name': row.name, 'phone_area': row.phone_area, 'secure': row.secure, 'timestamp': row.timestamp})
                                else:
                                        dict.append(
                                            {'pidm': row.pidm, 'name': row.name, 'timestamp': row.timestamp})

                        # _json = jsonify({"Tanimlar":dict})
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("sa query error! ", err)

        def add(self):
                        self.session.add(self.model)
                        self.session.commit()
                        print("Add Successfully")
                        return '', 204

                        # Add delete için response gerekmediğinden: The HTTP 204: No Content success status response code indicates that the request has succeeded, but that the client doesn't need to go away from its current page. A 204 response is cacheable by default. An ETag header is included in such a response

        def delete(self):
                try:
                        _pidm = int(self.model.pidm)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm).one()
                        self.session.delete(row)
                        self.session.commit()
                        print(row.name+" deleted successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404

        def getNextPidm(self):
                try:
                        dict = []

                        sql =  """
                                select nextval('sistemler_pidm_seq') pidm from gfox.public.sistemler limit 1
                                """

                        data = self.session.execute(sql)

                        for row in data:
                                dict.append({'pidm':row.pidm})
                                # bu fonksiyonun her çağırılışı db de değeri 2 arttırır.

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as err:
                        print("getNextPidm Query Error",err)
                        return '',404


# def addTanim(modelClass):
#         cc=Tanimlar(modelClass) # create class
#         return cc.add()

def getNextPidm(id):
    model = getModel(id)
    cc = Tanimlar(model)
    return cc.getNextPidm()

def getTanim(id):
    model = getModel(id)
    cc = Tanimlar(model)
    return cc.get()


def addTanim(form):
    _id = form.get('id')
    _name = form.get('name')
   # id=kvsistemler.. harici => local
    _local = str2bool(form.get("local"))
    # Güvenli Ülkeler
    _phone_area = form.get('phone_area')
    _secure = str2bool(form.get('secure'))

    model = getModel(_id)
    if (_id==TanimlarID.GuvenliUlkeler):
       cc=Tanimlar(model(name=_name, phone_area=_phone_area, secure=_secure))
    elif (_id==TanimlarID.KVSistemler):
       cc = Tanimlar(model(name=_name, local=_local))
    else:
       cc=Tanimlar(model(name=_name))

    return cc.add()

def deleteTanim(form):
    _id = form.get('id')
    _pidm = form.get('pidm')
#     print("Delete Tanım: ",_id,"/",_pidm)
    model = getModel(_id)
    cc=Tanimlar(model(pidm=_pidm)) # create class
    return cc.delete()


# if __name__ == "__main__":
#     e = SetProfiller()
#     e.add()

#     print("Successfully..")
