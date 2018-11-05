from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import SSDokumanlarModel

class SSDokumanlar():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def getSS(self, cid):
                try:
                        dict = []
                        dictDetay = [] # Dokumanlar

                        sql =  """
                                select pidm birim_pidm, name birim_name
                                from birimler
                                where cid=%d
                               """%(cid)

                        data = self.session.execute(sql)

                        for row in data:
                                dictDetay = self.getSSDetay(row.birim_pidm, cid)
                                dict.append({'birim_pidm':row.birim_pidm ,'birim_name':row.birim_name, 'dokumanlar':dictDetay})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)


        def getSSDetay(self, birim_pidm, cid): #Dokumanlar
                try:
                        dict = []

                        sql =  """
                                select ss_dokumanlar.pidm pidm,
                                        (select dokumanlar.name from dokumanlar where dokumanlar.pidm = ss_dokumanlar.dokuman_pidm limit 1) dokuman_name,
                                        (select ss_yayindurumu.name from ss_yayindurumu where ss_yayindurumu.pidm = ss_dokumanlar.yayin_pidm limit 1) yayin_name
                                from ss_dokumanlar
                                where ss_dokumanlar.birim_pidm=%d and ss_dokumanlar.cid=%d
                                """%(birim_pidm, cid)

                        data = self.session.execute(sql)

                        for row in data:
                                # dict.append({'pidm':row.pidm, 'birim':row.birim, 'kurum':row.kurum,'timestamp':row.timestamp})
                                dict.append({'pidm':row.pidm,'dokuman_name':row.dokuman_name, 'yayin_name':row.yayin_name})

                        return dict

                except Exception as e:
                        return Response("DB SQL Exception! ",e)

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("Add Successfully")
                        return '', 204
                except Exception as e:
                        return Response("SSDokumanlar DB Add Exception! ",e)

        def delete(self):
                try:
                        _pidm = int(self.model.pidm)
                        _cid = int(self.model.cid)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm, cid=_cid).one()
                        self.session.delete(row)
                        self.session.commit()
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getSSDokumanlar(cid):
    cc = SSDokumanlar(SSDokumanlarModel)
    return cc.getSS(cid)

def addSSDokuman(form):
     _birim_pidm = form.get('birim_pidm')
     _dokuman_pidm = form.get('dokuman_pidm')
     _yayin_pidm = form.get('yayin_pidm')
     _cid = form.get('cid')
     _uid = form.get('uid')

     cc=SSDokumanlar(SSDokumanlarModel(birim_pidm=_birim_pidm, dokuman_pidm=_dokuman_pidm, yayin_pidm=_yayin_pidm, cid=_cid, uid=_uid))

     return cc.add()

def delSSDokuman(form):
    _pidm = form.get('pidm')
    _cid = form.get('cid')

    cc=SSDokumanlar(SSDokumanlarModel(pidm=_pidm, cid=_cid))

    return cc.delete()