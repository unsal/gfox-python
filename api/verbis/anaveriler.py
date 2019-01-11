from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import *
from api.tanimlar.common import str2bool
from api.verbis.myconnection import MyConnection

#Temel connect, session, add, delete, getpidmname ve createdict için KVBase referans alındı...
class Anaveriler(MyConnection):
        def __init__(self, params):
                MyConnection.__init__(self)
                self.params = params

        def __del__(self):
                self.session.close()

        def get(self):
                try:
                        self.model = ModelViewAnaveriler
                        cid_ = self.params.get('cid')

                        dict = []

                        data = self.session.query(self.model).filter_by(cid=cid_)

                        for row in data:

                                kanallarData = self.createDict('kanallar', row.kanallar_data, cid_)
                                sistemlerData = self.createDict('sistemler', row.sistemler_data, cid_)
                                dayanaklarData = self.createDict('dayanaklar', row.dayanaklar_data, cid_)
                                islemeAmaclariData = self.createDict('isleme_amaclari', row.isleme_amaclari_data, cid_)
                                ortamlarData = self.createDict('ortamlar', row.ortamlar_data, cid_)
                                tedbirlerData = self.createDict('tedbirler', row.tedbirler_data, cid_)

                                dict.append({
                                        'pidm': row.pidm,

                                        'profil_pidm': row.profil_pidm,
                                        'profil_name': row.profil_name,

                                        'surec_pidm': row.surec_pidm,
                                        'surec_name': row.surec_name,

                                        'kv_pidm': row.kv_pidm,
                                        'kv_name': row.kv_name,

                                        'sure_pidm': row.sure_pidm,
                                        'sure_name': row.sure_name,

                                        'kanallar_data':kanallarData,
                                        'sistemler_data':sistemlerData,
                                        'dayanaklar_data':dayanaklarData,
                                        'isleme_amaclari_data':islemeAmaclariData,
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

        def add(self):
                try:
                        self.model = ModelAnaveriler()
                        params = self.params

                        self.model.profil_pidm = params.get('profil_pidm')
                        self.model.surec_pidm = params.get('surec_pidm')
                        self.model.kv_pidm = params.get('kv_pidm')
                        self.model.sure_pidm =  params.get('sure_pidm')
                        self.model.kanallar_data = params.get('kanallar_data')
                        self.model.sistemler_data = params.get('sistemler_data')
                        self.model.dayanaklar_data = params.get('dayanaklar_data')
                        self.model.isleme_amaclari_data = params.get('isleme_amaclari_data')
                        self.model.ortamlar_data = params.get('ortamlar_data')
                        self.model.tedbirler_data = params.get('tedbirler_data')
                        self.model.cid = params.get('cid')
                        self.model.uid = params.get('uid')

                        timestamp = datetime.today()
                        self.model.timestamp = timestamp

                        self.session.add(self.model)
                        self.session.commit()

                        print("insert successfully!")
                        return '', 204
                except Exception as err:
                        print("insert error !!! ", err)
                        return '', 404

        def update(self):
                try:
                        self.model = ModelAnaveriler
                        params = self.params
                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')
                        row = self.session.query(self.model).filter_by( pidm=pidm_, cid=cid_).one()

                        row.profil_pidm = params.get('profil_pidm')
                        row.surec_pidm = params.get('surec_pidm')
                        row.kv_pidm = params.get('kv_pidm')
                        row.sure_pidm = params.get('sure_pidm')
                        row.kanallar_data = params.get('kanallar_data')
                        row.sistemler_data = params.get('sistemler_data')
                        row.dayanaklar_data = params.get('dayanaklar_data')
                        row.isleme_amaclari_data = params.get('isleme_amaclari_data')
                        row.ortamlar_data = params.get('ortamlar_data')
                        row.tedbirler_data = params.get('tedbirler_data')
                        row.uid = params.get('uid')

                        timestamp = datetime.today()
                        row.timestamp = timestamp

                        self.session.commit()
                        print("update successfully!")
                        return '', 204
                except Exception as err:
                        print("update error !!! ", err)
                        return '', 404

        def delete(self):
                try:
                        self.model = ModelAnaveriler
                        params = self.params
                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')

                        row = self.session.query(self.model).filter_by( pidm=pidm_, cid=cid_).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("deleted successfully!")
                        return '', 204
                except Exception as err:
                        print("delete error !!! ", err)
                        return '', 404


def anaverilerAction(type, params):
        cc = Anaveriler(params)
        if (type=="get"):
                return cc.get()
        elif (type=="add"):
                return cc.add()
        elif (type=="update"):
                return cc.update()
        elif (type=="delete"):
                return cc.delete()
        else:
                return '', 404




