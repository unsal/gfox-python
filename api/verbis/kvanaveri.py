from flask import Response
from flask import jsonify
from db.model import KVAnaveriModel
from api.verbis.kvbase import KVBase

class KVAnaveri(KVBase):
        def __init__(self,modelClass):
                KVBase.__init__(self, modelClass)
                self.model = modelClass

        def get(self):
                try:
                        cid = self.model.cid
                        sql =  """
                               select
                                        base.pidm,
                                        (select birimler.name from birimler where birimler.pidm=base.birim_pidm limit 1) birim_name,
                                        (select kv.name from kv where kv.pidm=base.kv_pidm limit 1) kv_name,
                                        (select sureler.name from sureler where sureler.pidm=base.sure_pidm limit 1) sure_name,
                                        base.ulkeler_data,
                                        base.kanallar_data,
                                        base.dokumanlar_data,
                                        base.sistemler_data,
                                        base.dayanaklar_data,
                                        base.ortamlar_data
                                from    kv_anaveri base
                                where   base.cid = %d
                               """%(cid)

                        data = self.session.execute(sql)


                        dict = []
                        for row in data:
                                ulkelerData = self.createDict('ulkeler', row.ulkeler_data,cid ) #create as json[{pidm, name}]
                                kanallarData = self.createDict('kanallar', row.kanallar_data ,cid)
                                dokumanlarData = self.createDict('dokumanlar', row.dokumanlar_data ,cid)
                                sistemlerData = self.createDict('sistemler', row.sistemler_data,cid )
                                dayanaklarData = self.createDict('dayanaklar', row.dayanaklar_data,cid)
                                ortamlarData = self.createDict('ortamlar', row.ortamlar_data ,cid)

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
        def update(self, id, rowPidm, dataPidms, uid_):
                try:
                        row = self.session.query( self.model.__class__).filter_by(pidm=rowPidm).one()
                        row.uid=uid_

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


def get_kvanaveri(cid_):
    model = KVAnaveriModel(cid=cid_)
    cc = KVAnaveri(model)
    return cc.get()


def add_kvanaveri(data):

        birimPidm = data.get('birim_pidm')
        kvPidm = data.get('kv_pidm')
        surePidm = data.get('sure_pidm')
        cid_ = data.get('cid')
        uid_ = data.get('uid')

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
                                ortamlar_data=ortamlarData,
                                cid = cid_,
                                uid=uid_
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
        uid = data.get('uid')
        model = KVAnaveriModel()
        cc=KVAnaveri(model)

        return cc.update(id, rowPidm, dataPidms, uid)


