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
class Aktarimlar(KVBase):
        def __init__(self, model):
                KVBase.__init__(self, model)

        def __del__(self):
                self.session.close()

        def get(self, params):
                try:
                        cid_ = params.get('cid')
                        dict = []

                        data = self.session.query(self.model).filter_by(cid=cid_)

                        for row in data:
                                ulkelerData = self.createDict('ulkeler', row.ulkeler_data, cid_)
                                dayanaklarData = self.createDict('dayanaklar', row.dayanaklar_data, cid_)
                                paylasimAmaclariData = self.createDict('paylasim_amaclari', row.paylasim_amaclari_data, cid_)
                                paylasimSekilleriData = self.createDict('paylasim_sekilleri', row.paylasim_sekilleri_data, cid_)

                                dict.append({
                                        'pidm': row.pidm,
                                        'surec_pidm': row.surec_pidm,
                                        'surec_name': row.surec_name,
                                        'kv_pidm': row.kv_pidm,
                                        'kv_name': row.kv_name,
                                        'kurum_pidm': row.kurum_pidm,
                                        'kurum_name': row.kurum_name,

                                        'ulkeler_data':ulkelerData,
                                        'dayanaklar_data':dayanaklarData,
                                        'paylasim_amaclari_data':paylasimAmaclariData,
                                        'paylasim_sekilleri_data':paylasimSekilleriData,
                                        'yurtdisi':row.yurtdisi,
                                        'aciklama':row.aciklama,
                                        'bilgiveren':row.bilgiveren
                                })

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("****** ERROR ***********  aktarimlar get query error! ******** ", err)

        def add(self, params):
                try:
                        self.model.surec_pidm = params.get('surec_pidm')
                        self.model.kv_pidm = params.get('kv_pidm')
                        self.model.kurum_pidm =  params.get('kurum_pidm')
                        self.model.ulkeler_data = params.get('ulkeler_data')
                        self.model.dayanaklar_data = params.get('sistemler_data')
                        self.model.paylasim_amaclari_data = params.get('paylasim_amaclari_data')
                        self.model.paylasim_sekilleri_data = params.get('paylasim_sekilleri_data')

                        self.model.yurtdisi = params.get('yurtdisi')
                        self.model.aciklama = params.get('aciklama')
                        self.model.bilgiveren = params.get('bilgiveren')
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

        def update(self, params):
                try:
                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')
                        row = self.session.query(self.model).filter_by( pidm=pidm_, cid=cid_).one()

                        row.surec_pidm = params.get('surec_pidm')
                        row.kv_pidm = params.get('kv_pidm')
                        row.kurum_pidm = params.get('kurum_pidm')
                        row.ulkeler_data = params.get('ulkeler_data')
                        row.dayanaklar_data = params.get('dayanaklar_data')
                        row.paylasim_amaclari_data = params.get('paylasim_amaclari_data')
                        row.paylasim_sekilleri_data = params.get('paylasim_sekilleri_data')
                        row.yurtdisi = params.get('yurtdisi')
                        row.aciklama = params.get('aciklama')
                        row.bilgiveren = params.get('bilgiveren')
                        row.uid = params.get('uid')

                        timestamp = datetime.today()
                        row.timestamp = timestamp

                        self.session.commit()
                        print("update successfully!")
                        return '', 204
                except Exception as err:
                        print("update error !!! ", err)
                        return '', 404

        def delete(self, params):
                try:
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



def getAktarimlar(params):
    cc = Aktarimlar(ModelViewAktarimlar)
    return cc.get(params)

def updateAktarimlar(params):
    cc = Aktarimlar(ModelAktarimlar)
    return cc.update(params)

def deleteAktarimlar(params):
    cc = Aktarimlar(ModelAktarimlar)
    return cc.delete(params)

def addAktarimlar(params):
    cc = Aktarimlar(ModelAktarimlar())
    return cc.add(params)
