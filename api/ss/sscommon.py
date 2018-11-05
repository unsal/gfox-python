from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import SSKurumlarModel, SSKanallarModel, SSSistemlerModel

class SSCommon():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def getSS(self, cid):
                try:
                        dictBirimler = []
                        dictRelatedItems = []

                        sql =  """
                                select pidm birim_pidm, name birim_name
                                from birimler
                                where cid=%d
                               """%(cid)

                        data = self.session.execute(sql)

                        for row in data:
                                dictRelatedItems = self.getSSRelatedItems(row.birim_pidm, cid)
                                dictBirimler.append({'birim_pidm':row.birim_pidm ,'birim_name':row.birim_name, 'related_items':dictRelatedItems})

                        _json = jsonify(dictBirimler)

                        if (len(dictBirimler) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)


        def getSSRelatedItems(self, birim_pidm, cid): #Paylaşılan Kurumlar
                try:
                        dictRelatedItems = []

                        # related_item_pidm ve name react tarafında tek olarak yazılan ortak common component içindir.
                        sqlKurumlar =  """
                                select ss_kurumlar.pidm,
                                        (select kurumlar.pidm from kurumlar where kurumlar.pidm = ss_kurumlar.kurum_pidm limit 1) related_item_pidm,
                                        (select kurumlar.name from kurumlar where kurumlar.pidm = ss_kurumlar.kurum_pidm limit 1) related_item_name,
                                from ss_kurumlar
                                where ss_kurumlar.birim_pidm=%d and ss_kurumlar.acid=%d
                                """%(birim_pidm, cid)

                        # Kullanılan Sistmler
                        sqlSistemler =  """
                                select ss_kullanilan_sistemler.pidm,
                                        (select sistemler.pidm from sistemler where sistemler.pidm = ss_kullanilan_sistemler.sistem_pidm limit 1) related_item_pidm,
                                        (select sistemler.name from sistemler where sistemler.pidm = ss_kullanilan_sistemler.sistem_pidm limit 1) related_item_name
                                from ss_kullanilan_sistemler
                                where ss_kullanilan_sistemler.birim_pidm=%d and ss_kullanilan_sistemler.cid=%d
                                """%(birim_pidm, cid)

                        # Toplama Kanalları
                        sqlKanallar =  """
                                select ss_toplama_kanallari.pidm,
                                        (select kanallar.pidm from kanallar where kanallar.pidm = ss_toplama_kanallari.kanal_pidm limit 1) related_item_pidm,
                                        (select kanallar.name from kanallar where kanallar.pidm = ss_toplama_kanallari.kanal_pidm limit 1) related_item_name
                                from ss_toplama_kanallari
                                where ss_toplama_kanallari.birim_pidm=%d and ss_toplama_kanallari.cid=%d
                                """%(birim_pidm,cid)

                        if (self.model == SSKurumlarModel):
                                sql = sqlKurumlar
                        elif (self.model == SSSistemlerModel):
                                sql = sqlSistemler
                        elif (self.model == SSKanallarModel):
                                sql= sqlKanallar
                        else:
                                sql = ""


                        data = self.session.execute(sql)

                        # en baştaki pidm, ilgil tablodaki unique keydir.. react tarafında silmeyi yakalamak için..
                        for row in data:
                                dictRelatedItems.append({'pidm':row.pidm,'related_item_pidm':row.related_item_pidm, 'related_item_name':row.related_item_name})

                        return dictRelatedItems

                except Exception as e:
                        return Response("DB SQL Exception! ",e)

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("ADD Successfully")
                        return '', 204

                except Exception as e:
                        return Response("SSCommon DB Add Exception! ",e)

        def delete(self):
                try:
                        _pidm = int(self.model.pidm)
                        _cid = int(self.model.cid)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm, cid=_cid).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("DEL Successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getSSCommon(id, cid):
    if (id=='kurumlar'):
       cc = SSCommon(SSKurumlarModel)
    elif (id=='sistemler'):
       cc = SSCommon(SSSistemlerModel)
    elif (id=='kanallar'):
       cc = SSCommon(SSKanallarModel)
    else:
       cc = "str object"

    return cc.getSS(cid)

def deleteSSCommon(form):
    _id = form.get('id').strip() # trim..
    _pidm = form.get('pidm')
    _cid = form.get('cid')

    print('id: ',_id,'pidm: ', _pidm,'cid: ',_cid)

    if (_id=='kurumlar'):
        cc=SSCommon(SSKurumlarModel(pidm=_pidm, cid=_cid))
    elif (_id=='sistemler'):
        cc=SSCommon(SSSistemlerModel(pidm=_pidm, cid=_cid))
    elif (_id=='kanallar'):
        cc=SSCommon(SSKanallarModel(pidm=_pidm, cid=_cid))
    else:
        cc="str object" # value'nun özel bir anlamı yok, debugtaki hata buraya düşerse anla diye

#     print("id: ",_id)
#     return '',204
    return cc.delete()


def addSSCommon(form):
     _id =  form.get('id')
     _birim_pidm = form.get('birim_pidm')
     _related_item_pidm = form.get('related_item_pidm')
     _cid=form.get('cid')
     _uid=form.get('uid')

     if (_id=='kurumlar'):
         cc = SSCommon(SSKurumlarModel(birim_pidm=_birim_pidm, kurum_pidm=_related_item_pidm, cid=_cid, uid=_uid))
     elif (_id=='sistemler'):
        cc=SSCommon(SSSistemlerModel(birim_pidm=_birim_pidm, sistem_pidm = _related_item_pidm, cid=_cid, uid=_uid))
     elif (_id=='kanallar'):
        cc=SSCommon(SSKanallarModel(birim_pidm=_birim_pidm, kanal_pidm = _related_item_pidm, cid=_cid, uid=_uid))
     else:
        cc="str object" # value'nun özel bir anlamı yok, debugtaki hata buraya düşerse anla diye

     return cc.add()
