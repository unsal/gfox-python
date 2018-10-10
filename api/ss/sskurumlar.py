from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import SSKurumlarModel

class SSKurumlarClass():
        def __init__(self, modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def getSurecSahipleri(self):
                try:
                        dict = []
                        dictPK = [] # Paylaşılan Kurumlar

                        # SADECE SS_KURUMLAR Tablosundaki kayıtları getiririr
                        # sql =  """
                        #         select ss.birim_pidm birim_pidm, b.name birim_name
                        #         from ss_kurumlar ss, birimler b
                        #         where ss.birim_pidm = b.pidm
                        #         group by birim_pidm, birim_name
                        #        """

                        sql =  """
                                select pidm birim_pidm, name birim_name
                                from birimler
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                dictPK = self.getSurecSahipleriPK(row.birim_pidm)
                                dict.append({'birim_pidm':row.birim_pidm ,'birim_name':row.birim_name, 'kurumlar':dictPK})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response("NO DATA FOUND!")
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)


        def getSurecSahipleriPK(self, birim_pidm): #Paylaşılan Kurumlar
                try:
                        dict = []

                        sql =  """
                                select ss.pidm pidm, k.pidm kurum_pidm, k.name kurum_name
                                from ss_kurumlar ss, kurumlar k
                                where ss.kurum_pidm = k.pidm and
                                ss.birim_pidm=%s
                                """%(birim_pidm)

                        data = self.session.execute(sql)

                        for row in data:
                                # dict.append({'pidm':row.pidm, 'birim':row.birim, 'kurum':row.kurum,'timestamp':row.timestamp})
                                dict.append({'pidm':row.pidm,'kurum_pidm':row.kurum_pidm, 'kurum_name':row.kurum_name})

                        return dict
                        # _json = jsonify(dict)

                        # if (len(dict) == 0):
                        #         return Response("NO DATA FOUND!")
                        # else:
                        #         return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("Add Successfully")
                        return '', 204
                except Exception as e:
                        return Response("SSKurumlarClass DB Add Exception! ",e)

        def delete(self):
                try:
                        _pidm = int(self.model.pidm)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=_pidm).one()
                        self.session.delete(row)
                        self.session.commit()
                        print(row.name+" deleted successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404


def getSurecSahipleri():
    cc = SSKurumlarClass(SSKurumlarModel)
    return cc.getSurecSahipleri()

def addSSKurum(form):
     _birim_pidm = form.get('birim_pidm')
     _kurum_pidm = form.get('kurum_pidm')

     cc=SSKurumlarClass(SSKurumlarModel(birim_pidm=_birim_pidm, kurum_pidm=_kurum_pidm))

     return cc.add()

def delSSKurum(form):
    _pidm = form.get('pidm')

    cc=SSKurumlarClass(SSKurumlarModel(pidm=_pidm))

    return cc.delete()