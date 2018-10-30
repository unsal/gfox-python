from flask import Response
from flask import jsonify
from db.model import KVPaylasimModel
from api.verbis.kvbase import KVBase

class KVPaylasim(KVBase):
        def __init__(self,modelClass):
                KVBase.__init__(self, modelClass)

        def get(self):

                try:
                        dict = []

                        sql =  """
                                select  base.pidm,
                                        birimler.name birim_name,
                                        kv.name kv_name,
                                        kurumlar.name kurum_name,
                                        base.islemeamaclari_data,
                                        base.paylasimamaclari_data,
                                        base.paylasimsekilleri_data
                                from    kv_paylasim base, birimler, kv, kurumlar
                                where   base.birim_pidm=birimler.pidm and
                                        base.kv_pidm = kv.pidm and
                                        base.kurum_pidm = kurumlar.pidm
                                order by base.timestamp desc
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                iaData = self.createDict('isleme_amaclari', row.islemeamaclari_data ) #create as json[{pidm, name}]
                                paData = self.createDict('paylasim_amaclari', row.paylasimamaclari_data )
                                psData = self.createDict('paylasim_sekilleri', row.paylasimsekilleri_data )
                                # str = json.dumps(data)
                                # print('IA: ',iaData)
                                # print('PA: ',paData)
                                # print('PS: ',paylasimSekilleriData)

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
        def update(self, id, rowPidm, dataPidms):
                try:
                        row = self.session.query( self.model.__class__).filter_by(pidm=rowPidm).one()

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


def get_kvpaylasim():
    cc = KVPaylasim(KVPaylasimModel)
    return cc.get()


def add_kvpaylasim(data):

        birimPidm = data.get('birim_pidm')
        kvPidm = data.get('kv_pidm')
        kurumPidm = data.get('kurum_pidm')
        iaData = data.get('islemeamaclari_data')
        paData = data.get('paylasimamaclari_data')
        paylasimSekilleriData = data.get('paylasimsekilleri_data')

        # return ""
        model = KVPaylasimModel(birim_pidm=birimPidm,
                                kv_pidm = kvPidm,
                                kurum_pidm=kurumPidm,
                                islemeamaclari_data = iaData,
                                paylasimamaclari_data=paData,
                                paylasimsekilleri_data=paylasimSekilleriData )
        cc=KVPaylasim(model)
        return cc.add()


def update_kvpaylasim(id, data):
# silinen kv datasını (json) veritabanında günceller

        rowPidm = data.get('pidm')
        dataPidms = data.get('data')
        model = KVPaylasimModel()
        cc=KVPaylasim(model)

        return cc.update(id, rowPidm, dataPidms)

def delete_kvpaylasim(data):
  # silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        model = KVPaylasimModel(pidm=pidm_)
        cc=KVPaylasim(model)

        print('pidm: ', pidm_)

        return cc.delete()
