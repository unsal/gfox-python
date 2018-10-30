from flask import Response
from flask import jsonify
from db.model import KVAnaveriModel
from api.verbis.kvbase import KVBase

class KVAnaveri(KVBase):
        def __init__(self,modelClass):
                KVBase.__init__(self, modelClass)

        def get(self):
                try:
                        dict = []

                        sql =  """
                               select
                                        base.pidm,
                                        birimler.name birim_name,
                                        kv.name kv_name,
                                        sureler.name sure_name,
                                        base.ulkeler_data,
                                        base.kanallar_data,
                                        base.dokumanlar_data,
                                        base.sistemler_data,
                                        base.dayanaklar_data,
                                        base.ortamlar_data
                                from
                                        kv_anaveri base, birimler, kv,
                                        sureler
                                where
                                        base.birim_pidm = birimler.pidm and
                                        base.kv_pidm = kv.pidm and
                                        base.sure_pidm = sureler.pidm
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                ulkelerData = self.createDict('ulkeler', row.ulkeler_data ) #create as json[{pidm, name}]
                                kanallarData = self.createDict('kanallar', row.kanallar_data )
                                dokumanlarData = self.createDict('dokumanlar', row.dokumanlar_data )
                                sistemlerData = self.createDict('sistemler', row.sistemler_data )
                                dayanaklarData = self.createDict('dayanaklar', row.dayanaklar_data )
                                ortamlarData = self.createDict('ortamlar', row.ortamlar_data )

                                dict.append({'pidm':row.pidm,
                                                'birim_name':row.birim_name ,
                                                'kv_name':row.kv_name,
                                                'sure_name':row.sure_name,
                                                'ulkeler_data':ulkelerData,
                                                'kanallar_data':kanallarData,
                                                'dokumanlar_data':dokumanlarData,
                                                'sistemler_data':sistemlerData,
                                                'dayanaklar_data':dayanaklarData,
                                                'ortamlar_data':ortamlarData
                                        })

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("KVAnaveri().get() -> DB SQL Exception! ",e)

        # kvbase'deki update tek bir data fielde göre çalıştığı için ayrıca eklendi bu..
        def update(self, id, rowPidm, dataPidms):
                try:
                        row = self.session.query( self.model.__class__).filter_by(pidm=rowPidm).one()
                        if (id=='ulkeler'):
                                row.ulkeler_data = dataPidms
                        elif (id=='kanallar'):
                                row.kanallar_data = dataPidms
                        elif (id=='dokumanlar'):
                                row.dokumanlar_data = dataPidms
                        elif (id=='sistemler'):
                                row.sistemler_data = dataPidms
                        elif (id=='dayanaklar'):
                                row.dayanaklar_data = dataPidms
                        elif (id=='ortamlar'):
                                row.ortamlar_data = dataPidms
                        else:
                                return None

                        self.session.commit()
                        print("update successfully!")
                        return '', 204
                except Exception as err:
                        print("DB Error on KVAnaveri->update ", err)
                        return '', 404


def get_kvanaveri():
    model = KVAnaveriModel()
    cc = KVAnaveri(model)
    return cc.get()


def add_kvanaveri(data):

        birimPidm = data.get('birim_pidm')
        kvPidm = data.get('kv_pidm')
        surePidm = data.get('sure_pidm')

        ulkelerData = data.get('ulkeler_data')
        kanallarData = data.get('kanallar_data')
        dokumanlarData = data.get('dokumanlar_data')
        sistemlerData = data.get('sistemler_data')
        dayanaklarData = data.get('dayanaklar_data')
        ortamlarData = data.get('ortamlar_data')

        # return ""
        model = KVAnaveriModel(birim_pidm=birimPidm,
                                kv_pidm = kvPidm,
                                sure_pidm=surePidm,
                                ulkeler_data = ulkelerData,
                                kanallar_data=kanallarData,
                                dokumanlar_data=dokumanlarData,
                                sistemler_data=sistemlerData,
                                dayanaklar_data=dayanaklarData,
                                ortamlar_data=ortamlarData
                                )
        cc=KVAnaveri(model)
        return cc.add()

def delete_kvanaveri(data):
  # silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        model = KVAnaveriModel(pidm=pidm_)
        cc=KVAnaveri(model)

        return cc.delete()


def update_kvanaveri(id, data):
# silinen kv datasını (json) veritabanında günceller

        rowPidm = data.get('pidm')
        dataPidms = data.get('data')
        model = KVAnaveriModel()
        cc=KVAnaveri(model)

        return cc.update(id, rowPidm, dataPidms)


