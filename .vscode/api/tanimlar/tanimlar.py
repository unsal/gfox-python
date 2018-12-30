from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Ortamlar, Sureler, Kurumlar, Dayanaklar, PaylasimAmaclari, PaylasimSekilleri, Ulkeler, TanimlarID, getModel, YayinDurumlari
from api.tanimlar.common import str2bool

class Tanimlar():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                # !!!modelClass() parentezle yaparsan class create edilir, bu koşulda olmaz...
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def get(self, cid_):
                try:
                        dict = []

                        if (self.model == Sistemler):
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.local, self.model.timestamp).filter_by(cid=cid_)
                        elif (self.model == Ulkeler):
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.phone_area, self.model.secure, self.model.timestamp).filter_by(cid=cid_)
                        elif (self.model == YayinDurumlari): # myComponent > CreateYayindurumlariOptions için
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.timestamp)
                        else:
                                data = self.session.query(
                                    self.model.pidm, self.model.name, self.model.timestamp).filter_by(cid=cid_)


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
                        _cid = int(self.model.cid)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm, cid=_cid).one()
                        self.session.delete(row)
                        self.session.commit()
                        print(row.name+" deleted successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


# def addTanim(modelClass):
#         cc=Tanimlar(modelClass) # create class
#         return cc.add()

def getTanim(id, cid):
    model = getModel(id)
    cc = Tanimlar(model)
    return cc.get(cid)


def addTanim(form):
    _id = form.get('id')
    _name = form.get('name')
    _local = str2bool(form.get("local"))
    _phone_area = form.get('phone_area')
    _secure = str2bool(form.get('secure'))
    # auth
    _cid = form.get('cid')
    _uid = form.get('uid')
#     print("cid: ",_cid)
#     print("uid: ",_uid)

    model = getModel(_id)
    if (_id==TanimlarID.GuvenliUlkeler):
       cc=Tanimlar(model(name=_name, phone_area=_phone_area, secure=_secure, cid=_cid, uid=_uid))
    elif (_id==TanimlarID.KVSistemler):
       cc = Tanimlar(model(name=_name, local=_local, cid=_cid, uid=_uid))
    else:
       cc=Tanimlar(model(name=_name, cid=_cid, uid=_uid))

    return cc.add()

def deleteTanim(form):
    _id = form.get('id')
    _pidm = form.get('pidm')
    _cid = form.get('cid')
#     print("Delete Tanım: ",_id,"/",_pidm)
    model = getModel(_id)
    cc=Tanimlar(model(pidm=_pidm, cid=_cid)) # create class
    return cc.delete()


# if __name__ == "__main__":
#     e = SetProfiller()
#     e.add()

#     print("Successfully..")
