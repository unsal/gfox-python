from flask import Response
from flask import jsonify
from db.model import KVProfilModel
from api.verbis.kvbase import KVBase
from db.connection import Connect
from array import array

class KVProfil(KVBase):
        def __init__(self,model):
                KVBase.__init__(self, model)
                # self.model = model

        def get(self, cid):
                try:
                        sql =  """
                                select  pidm, profil_name, birim_name,data
                                from    view_kvprofil
                                where   cid=%d
                                order by timestamp desc
                               """%(cid)

                        data = self.session.execute(sql)

                        dict = []
                        for row in data:
                                kvData = self.createDict('kv',row.data, cid)
                                # str = json.dumps(data)
                                dict.append({'pidm':row.pidm,'profil_name':row.profil_name ,'birim_name':row.birim_name, 'data':kvData})

                        _json = jsonify(dict)

                        print('json: ', _json)
                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("KVProfil().get2() -> SQLAlchemy Exception! ",e)


def get_kvprofil(cid):
    cc=KVProfil(KVProfilModel)
    return cc.get(cid)

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
