from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
import json
from array import array
from sqlalchemy.inspection import inspect
from db.model import *


class Envanter ():
        def __init__(self):
                self.model = ModelEnvanter
                self.conn = Connect()
                self.session = self.conn.session()

        def __del__(self):
                self.session.close()

        # GET query results
        def get(self, params):
                try:
                        id =  params.get('id') #anaveriler, aktarimlar
                        cid_ = params.get('cid')
                        uid_ = params.get('uid')

                        result = self.session.query(self.model).filter_by(cid=cid_, uid=uid_)

                        if (id=="anaveriler"):
                                dataf = ['profil','birim','bolum','surec','kv','sure', \
                                        'ortamlar_data','tedbirler_data','kanallar_data','sistemler_data','dayanaklar_data','isleme_amaclari_data']
                        elif (id=="aktarimlar"):
                                dataf = ['profil','birim','bolum','surec','kv','sure', \
                                        'ortamlar_data','tedbirler_data','kanallar_data','sistemler_data','dayanaklar_data','isleme_amaclari_data']
                        else:
                                dataf= None
                                return '',202

                        dict = []
                        for row in result:
                                myRow = {}

                                #pidm, cid, uid, timestamp için..
                                instance = inspect(row)
                                for key, item in instance.attrs.items():
                                        if (key not in ['data','timestamp']):
                                                myRow[key] = item.value

                                #json data alanı için
                                for k in dataf:
                                        myRow[k] = row.data[k]

                                dict.append(myRow)

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("!!! Query ERROR !!!", err)


        def update(self, params):
                try:
                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')
                        # uid_ = params.get('uid')
                        row = self.session.query(self.model).filter_by( pidm=pidm_, cid=cid_)

                        row.update(params)

                        self.session.commit()
                        print("*** UPDATE successfully ***")
                        return '', 204
                except Exception as err:
                        print("!!! UPDATE error !!! ", err)
                        return '', 404

        def add(self, params):
                try:
                        record = []
                        record.append(params)

                        for row in record:
                                self.session.add(self.model(**row))

                        self.session.commit()

                        print("*** Record ADD successfully *** ")
                        return '', 204
                except Exception as err:
                        print("!!! Record ADD ERROR !!! ", err)
                        return '', 404

        def delete(self, params):
                try:

                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')

                        row = self.session.query(self.model).filter_by( pidm=pidm_, cid=cid_).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("*** Record DELETED successfully ***")
                        return '', 204
                except Exception as err:
                        print("!!! ERROR ON DELETE !!! ", err)
                        return '', 404

def actionEnvanter(params, type):
        cc = Envanter()
        if (type=="get"):
                return cc.get(params)
        elif (type=="add"):
                return cc.add(params)
        elif (type=="update"):
                return cc.update(params)
        elif (type=="delete"):
                return cc.delete(params)
        else:
                return '', 404
