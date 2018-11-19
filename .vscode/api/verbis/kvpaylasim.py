from flask import Response
from flask import jsonify
from db.model import KVPaylasimModel
from api.verbis.kvbase import KVBase

class KVPaylasim(KVBase):
        def __init__(self,model):
                KVBase.__init__(self, model)
                # self.model = modelClass

        def get(self, cid):

                try:
                        sql =  """
                                select  pidm, birim_name, kv_name, kurum_name, islemeamaclari_data, paylasimamaclari_data, paylasimsekilleri_data
                                from    view_kvpaylasim
                                where   cid=%d
                                order by timestamp desc
                               """%(cid)

                        data = self.session.execute(sql)

                        dict = []
                        for row in data:
                                iaData = self.createDict('isleme_amaclari', row.islemeamaclari_data,cid ) #create as json[{pidm, name}]
                                paData = self.createDict('paylasim_amaclari', row.paylasimamaclari_data,cid )
                                psData = self.createDict('paylasim_sekilleri', row.paylasimsekilleri_data,cid )

                                dict.append({'pidm':row.pidm,
                                                'birim_name':row.birim_name ,
                                                'kv_name':row.kv_name,
                                                'kurum_name':row.kurum_name,
                                                'ia_data':iaData, #islemeamaci_pidm
                                                'pa_data':paData, #paylasimamaci_pidm
                                                'ps_data':psData #paylasimsekli_pidm
                                        })

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("KVPaylasim().get() -> DB SQL Exception! ",e)

        # kvbase'deki update tek bir data fielde göre çalıştığı için ayrıca eklendi bu..
        def update(self, id, rowPidm, dataPidms, uid):
                try:
                        row = self.session.query( self.model.__class__).filter_by(pidm=rowPidm).one()

                        row.uid = uid  #user id update

                        if (id=='ia'):
                                row.islemeamaclari_data = dataPidms
                        elif (id=='pa'):
                                row.paylasimamaclari_data = dataPidms
                        elif (id=='ps'):
                                row.paylasimsekilleri_data = dataPidms
                        else:
                                return None

                        self.session.commit()
                        print("update successfully!")
                        return '', 204
                except Exception as err:
                        print("DB Error on kvpaylasim->update ", err)
                        return '', 404

def get_kvpaylasim(cid):
    cc = KVPaylasim(KVPaylasimModel)
    return cc.get(cid)


def add_kvpaylasim(data):

        birimPidm = data.get('birim_pidm')
        kvPidm = data.get('kv_pidm')
        kurumPidm = data.get('kurum_pidm')
        iaData = data.get('islemeamaclari_data')
        paData = data.get('paylasimamaclari_data')
        paylasimSekilleriData = data.get('paylasimsekilleri_data')
        cid_ = data.get('cid')
        uid_ = data.get('uid')

        # return ""
        model = KVPaylasimModel(birim_pidm=birimPidm,
                                kv_pidm = kvPidm,
                                kurum_pidm=kurumPidm,
                                islemeamaclari_data = iaData,
                                paylasimamaclari_data=paData,
                                paylasimsekilleri_data=paylasimSekilleriData,
                                cid=cid_, uid=uid_)
        cc=KVPaylasim(model)
        return cc.add()


def update_kvpaylasim(id, data):
# silinen kv datasını (json) veritabanında günceller

        rowPidm = data.get('pidm')
        dataPidms = data.get('data')
        uid = data.get('uid')
        model = KVPaylasimModel()
        cc=KVPaylasim(model)

        return cc.update(id, rowPidm, dataPidms, uid)

def delete_kvpaylasim(data):
  # silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        model = KVPaylasimModel(pidm=pidm_)
        cc=KVPaylasim(model)

        print('pidm: ', pidm_)

        return cc.delete()
