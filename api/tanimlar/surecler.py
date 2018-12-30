from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import ModelViewSurecler, ModelSurecler
from api.tanimlar.common import str2bool

class Surecler():
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

                        data = self.session.query(self.model.birim_name, self.model.bolum_name, self.model.bolum_pidm, self.model.surecler_data).filter_by(cid=cid_)
                        # data = data.order_by(self.model.birim_name)

                        for row in data:
                                dict.append( {'birim_name': row.birim_name, 'bolum_name': row.bolum_name, 'bolum_pidm': row.bolum_pidm, 'surecler_data': row.surecler_data})

                        # _json = jsonify({"Bolumler":dict})
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("surecler get query error! ", err)

        def getDropdownSurecler(self, cid_):
                try:
                        dict = []

                        data = self.session.query(self.model.pidm, self.model.name).filter_by(cid=cid_)
                        # data = data.order_by(self.model.birim_name)

                        for row in data:
                                dict.append( {'pidm': row.pidm, 'name': row.name})

                        # _json = jsonify({"Bolumler":dict})
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("surecler dropdown get query error! ", err)

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("Surecler ADD Successfully")
                        return '', 204

                except Exception as e:
                        return Response("Surecler Add Exception!! ",e)

        def delete(self):
                try:
                        pidm_ = int(self.model.pidm)
                        cid_ = int(self.model.cid)

                        row = self.session.query(self.model.__class__).filter_by(pidm=pidm_, cid=cid_).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("surec deleted successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getSurecler(cid):
    model = ModelViewSurecler
    cc = Surecler(model)
    return cc.get(cid)

def getDropdownSurecler(cid):
    model = ModelSurecler
    cc = Surecler(model)
    return cc.getDropdownSurecler(cid)

def addSurec(data):

        bolumPidm = data.get('bolum_pidm')
        surecName = data.get('name')
        cid_ = data.get('cid')
        uid_ = data.get('uid')

        # return ""
        model = ModelSurecler(bolum_pidm=bolumPidm, name = surecName, cid=cid_, uid=uid_ )
        cc=Surecler(model)
        return cc.add()

def deleteSurec(data):
        pidm_ = data.get('pidm')
        cid_ = data.get('cid')

        model = ModelSurecler(pidm=pidm_, cid=cid_)
        cc=Surecler(model)

        return cc.delete()