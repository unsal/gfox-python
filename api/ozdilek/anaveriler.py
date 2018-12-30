from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import *
from api.tanimlar.common import str2bool
from api.verbis.kvbase import KVBase

#Temel connect, session, add, delete, getpidmname ve createdict için KVBase referans alındı...
class Anaveriler(KVBase):
        def __init__(self, model):
                KVBase.__init__(self, model)

        def __del__(self):
                self.session.close()

        def get(self, cid_):
                try:
                        dict = []

                        data = self.session.query(self.model).filter_by(cid=cid_)

                        for row in data:
                                ortamlarData = self.createDict('ortamlar', row.ortamlar_data, cid_)
                                tedbirlerData = self.createDict('tedbirler', row.tedbirler_data, cid_)
                                dict.append({
                                        'pidm': row.pidm,
                                        'profil_name': row.profil_name,
                                        'surec_name': row.surec_name,
                                        'kv_name': row.kv_name,
                                        'sure_name': row.sure_name,
                                        'kanal_name': row.kanal_name,
                                        'sistem_name': row.sistem_name,
                                        'dayanak_name':row.dayanak_name,
                                        'isleme_amaclari_name':row.isleme_amaclari_name,
                                        'ortamlar_data':ortamlarData,
                                        'tedbirler_data':tedbirlerData
                                })

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("anaveriler get query error! ", err)

        def update(self, id, rowPidm, data, cid_, uid_):
                try:

                        row = self.session.query(self.model).filter_by(
                            pidm=rowPidm, cid=cid_).one()

                        row.uid = uid_

                        if (id == 'ortamlar'):
                                row.ortamlar_data = data
                        elif (id == 'tedbirler'):
                                row.tedbirler_data = data
                        else:
                           return None

                        self.session.commit()
                        print("update successfully!")
                        return '', 204
                except Exception as err:
                        print("update error !!! ", err)
                        return '', 404



def getAnaveriler(cid):
    model = ModelViewAnaveriler
    cc = Anaveriler(model)
    return cc.get(cid)

def updateAnaveriler(data):
    id = data.get('id')
    pidm = data.get('pidm')
    datacell = data.get('data')
    cid = data.get('cid')
    uid = data.get('uid')

    model = ModelAnaveriler
    cc = Anaveriler(model)

    return cc.update(id, pidm, datacell, cid, uid)
