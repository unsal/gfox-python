from flask import Response
from flask import jsonify
from db.model import KVProfilModel
from api.verbis.kvbase import KVBase

class KVProfil(KVBase):
        def __init__(self,modelClass):
                KVBase.__init__(self, modelClass)

        def get(self):
                try:
                        dict = []

                        sql =  """
                                select  base.pidm, p.name profil_name, b.name birim_name, base.data
                                from    kv_profil base, profiller p, birimler b
                                where   base.profil_pidm=p.pidm and base.birim_pidm = b.pidm
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                kvData = self.createDict('kv',row.data)
                                # str = json.dumps(data)
                                dict.append({'pidm':row.pidm,'profil_name':row.profil_name ,'birim_name':row.birim_name, 'data':kvData})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("KVProfil().get() -> DB SQL Exception! ",e)


def get_kvprofil():
    cc = KVProfil(KVProfilModel)
    return cc.get()


def add_kvprofil(data):

        profilPidm = data.get('profil_pidm')
        birimPidm = data.get('birim_pidm')
        dataKv = data.get('data')

        # return ""
        model = KVProfilModel(profil_pidm=profilPidm, birim_pidm = birimPidm, data = dataKv )
        cc=KVProfil(model)
        return cc.add()


def update_kvprofil(data):
# silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        dataKv = data.get('data')
        model = KVProfilModel(pidm=pidm_, data=dataKv)
        cc=KVProfil(model)

        return cc.update()

def delete_kvprofil(data):
  # silinen kv datasını (json) veritabanında günceller
        pidm_ = data.get('pidm')
        model = KVProfilModel(pidm=pidm_)
        cc=KVProfil(model)

        return cc.delete()
