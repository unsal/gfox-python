from flask import Response
from flask import jsonify
from db.model import KVProfilModel
from api.verbis.kvbase import KVBase

class KVProfil(KVBase):
        def __init__(self,modelClass):
                KVBase.__init__(self, modelClass)
                self.model = modelClass

        def get(self):
                try:
                        cid = self.model.cid
                        dict = []

                        sql =  """
                                select  base.pidm,
                                        (select profiller.name from profiller where profiller.pidm = base.profil_pidm limit 1) profil_name,
                                        (select birimler.name from birimler where birimler.pidm =  base.birim_pidm limit 1) birim_name,
                                        base.data
                                from    kv_profil base
                                where   base.cid = %d
                               """%(cid)

                        data = self.session.execute(sql)

                        for row in data:
                                kvData = self.createDict('kv',row.data, cid)
                                # str = json.dumps(data)
                                dict.append({'pidm':row.pidm,'profil_name':row.profil_name ,'birim_name':row.birim_name, 'data':kvData})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("KVProfil().get() -> DB SQL Exception! ",e)


def get_kvprofil(cid_):
    model = KVProfilModel(cid=cid_)
    cc=KVProfil(model)
    return cc.get()


def add_kvprofil(data):

        profilPidm = data.get('profil_pidm')
        birimPidm = data.get('birim_pidm')
        dataKv = data.get('data')
        cid_ = data.get('cid')
        uid_ = data.get('uid')

        # return ""
        model = KVProfilModel(profil_pidm=profilPidm, birim_pidm = birimPidm, data = dataKv, cid=cid_, uid=uid_ )
        cc=KVProfil(model)
        return cc.add()


def update_kvprofil(data):
# silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        dataKv = data.get('data')
        uid_ = data.get('uid')
        model = KVProfilModel(pidm=pidm_, data=dataKv, uid=uid_)
        cc=KVProfil(model)

        return cc.update()

def delete_kvprofil(data):
  # silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        model = KVProfilModel(pidm=pidm_)
        cc=KVProfil(model)

        return cc.delete()
