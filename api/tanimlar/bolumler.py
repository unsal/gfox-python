from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import ModelViewBolumler, ModelBolumler
from api.tanimlar.common import str2bool

class Bolumler():
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

                        data = self.session.query(self.model.birim_pidm, self.model.birim_name, self.model.bolumler_data).filter_by(cid=cid_)
                        # data = data.order_by(self.model.birim_name)

                        for row in data:
                                dict.append( {'birim_pidm': row.birim_pidm, 'birim_name': row.birim_name, 'bolumler_data': row.bolumler_data})

                        # _json = jsonify({"Bolumler":dict})
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("sa query error! ", err)

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("Bolumler ADD Successfully")
                        return '', 204

                except Exception as e:
                        return Response("Bolumler Add Exception!! ",e)

        def delete(self):
                try:
                        birim_pidm_ = int(self.model.birim_pidm)
                        pidm_ = int(self.model.pidm)
                        cid_ = int(self.model.cid)

                        row = self.session.query(self.model.__class__).filter_by(birim_pidm=birim_pidm_, pidm=pidm_, cid=cid_).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("bolum deleted successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getBolumler(cid):
    model = ModelViewBolumler
    cc = Bolumler(model)
    return cc.get(cid)

def addBolum(data):

        birimPidm = data.get('birim_pidm')
        bolumName = data.get('name')
        cid_ = data.get('cid')
        uid_ = data.get('uid')

        print('Birim Pidm: ', birimPidm)
        print('Bölüm name: ',bolumName)
        print('cid: ', cid_)
        print('uid: ', uid_)

        # return ""
        model = ModelBolumler(birim_pidm=birimPidm, name = bolumName, cid=cid_, uid=uid_ )
        cc=Bolumler(model)
        return cc.add()

def deleteBolum(data):
        birim_pidm_ = data.get('birim_pidm')
        pidm_ = data.get('pidm')
        cid_ = data.get('cid')

        model = ModelBolumler(birim_pidm=birim_pidm_, pidm=pidm_, cid=cid_)
        cc=Bolumler(model)

        return cc.delete()