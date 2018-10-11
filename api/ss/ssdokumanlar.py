from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import SSDokumanlarModel

class SSDokumanlarClass():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def getSS(self):
                try:
                        dict = []
                        dictDetay = [] # Dokumanlar

                        sql =  """
                                select pidm birim_pidm, name birim_name
                                from birimler
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                dictDetay = self.getSSDetay(row.birim_pidm)
                                dict.append({'birim_pidm':row.birim_pidm ,'birim_name':row.birim_name, 'dokumanlar':dictDetay})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response("NO DATA FOUND!")
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)


        def getSSDetay(self, birim_pidm): #Dokumanlar
                try:
                        dict = []

                        sql =  """
                                select ss.pidm pidm, d.name dokuman_name, y.name yayin_name
                                from ss_dokumanlar ss, dokumanlar d, ss_yayindurumu y
                                where ss.dokuman_pidm = d.pidm and ss.yayin_pidm = y.pidm and
                                ss.birim_pidm=%s
                                """%(birim_pidm)

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
                        return Response("SSDokumanlarClass DB Add Exception! ",e)

        def delete(self):
                try:
                        _pidm = int(self.model.pidm)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm).one()
                        self.session.delete(row)
                        self.session.commit()
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getSSDokumanlar():
    cc = SSDokumanlarClass(SSDokumanlarModel)
    return cc.getSS()

def addSSDokuman(form):
     _birim_pidm = form.get('birim_pidm')
     _kurum_pidm = form.get('kurum_pidm')

     cc=SSDokumanlarClass(SSDokumanlarModel(birim_pidm=_birim_pidm, kurum_pidm=_kurum_pidm))

     return cc.add()

def delSSDokuman(form):
    _pidm = form.get('pidm')

    cc=SSDokumanlarClass(SSDokumanlarModel(pidm=_pidm))

    return cc.delete()