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

        def getSS(self):
                try:
                        dictBirimler = []
                        dictRelatedItems = []

                        sql =  """
                                select pidm birim_pidm, name birim_name
                                from birimler
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                dictRelatedItems = self.getSSRelatedItems(row.birim_pidm)
                                dictBirimler.append({'birim_pidm':row.birim_pidm ,'birim_name':row.birim_name, 'related_items':dictRelatedItems})

                        _json = jsonify(dictBirimler)

                        if (len(dictBirimler) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)


        def getSSRelatedItems(self, birim_pidm): #Paylaşılan Kurumlar
                try:
                        dictRelatedItems = []

                        # related_item_pidm ve name react tarafında tek olarak yazılan ortak common component içindir.
                        sqlKurumlar =  """
                                select ss.pidm pidm, k.pidm related_item_pidm, k.name related_item_name
                                from ss_kurumlar ss, kurumlar k
                                where ss.kurum_pidm = k.pidm and
                                ss.birim_pidm=%s
                                """%(birim_pidm)

                        # Kullanılan Sistmler
                        sqlSistemler =  """
                                select ss.pidm pidm, s.pidm related_item_pidm, s.name related_item_name
                                from ss_kullanilan_sistemler ss, sistemler s
                                where ss.sistem_pidm = s.pidm and
                                ss.birim_pidm=%s
                                """%(birim_pidm)

                        # Toplama Kanalları
                        sqlKanallar =  """
                                select ss.pidm pidm, k.pidm related_item_pidm, k.name related_item_name
                                from ss_toplama_kanallari ss, kanallar k
                                where ss.kanal_pidm = k.pidm and
                                ss.birim_pidm=%s
                                """%(birim_pidm)

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
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("DEL Successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getSSCommon(id):
    if (id=='kurumlar'):
       cc = SSCommon(SSKurumlarModel)
    elif (id=='sistemler'):
       cc = SSCommon(SSSistemlerModel)
    elif (id=='kanallar'):
       cc = SSCommon(SSKanallarModel)
    else:
       cc = "str object"

    return cc.getSS()

def deleteSSCommon(form):
    _id = form.get('id').strip() # trim..
    _pidm = form.get('pidm')

    if (_id=='kurumlar'):
        cc=SSCommon(SSKurumlarModel(pidm=_pidm))
    elif (_id=='sistemler'):
        cc=SSCommon(SSSistemlerModel(pidm=_pidm))
    elif (_id=='kanallar'):
        cc=SSCommon(SSKanallarModel(pidm=_pidm))
    else:
        cc="str object" # value'nun özel bir anlamı yok, debugtaki hata buraya düşerse anla diye

#     print("id: ",_id)
#     return '',204
    return cc.delete()


def addSSCommon(form):
     _id =  form.get('id')
     _birim_pidm = form.get('birim_pidm')
     _related_item_pidm = form.get('related_item_pidm')

     if (_id=='kurumlar'):
         cc = SSCommon(SSKurumlarModel(birim_pidm=_birim_pidm, kurum_pidm=_related_item_pidm))
     elif (_id=='sistemler'):
        cc=SSCommon(SSSistemlerModel(birim_pidm=_birim_pidm, sistem_pidm = _related_item_pidm))
     elif (_id=='kanallar'):
        cc=SSCommon(SSKanallarModel(birim_pidm=_birim_pidm, kanal_pidm = _related_item_pidm))
     else:
        cc="str object" # value'nun özel bir anlamı yok, debugtaki hata buraya düşerse anla diye

     return cc.add()
