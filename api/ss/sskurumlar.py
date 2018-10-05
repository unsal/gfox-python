from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from datetime import datetime
from db.model import SSKurumlar


class SSKurumlarClass():
        def __init__(self):
                self.conn = Connect()
                self.session = self.conn.session()

        def __del__(self):
                self.session.close()

        def getSurecSahipleri(self):
                try:
                        dict = []

                        # sql =  """
                        #         select ss.pidm, b.name birim, k.name kurum, ss.timestamp
                        #         from ss_kurumlar ss, birimler b, kurumlar k
                        #         where ss.birim_pidm = b.pidm and ss.kurum_pidm = k.pidm
                        #         order by ss.timestamp
                        #         """
                        sql =  """
                                select ss.birim_pidm birim_pidm, b.name birim_name
                                from ss_kurumlar ss, birimler b
                                where ss.birim_pidm = b.pidm
                                group by birim_pidm, birim_name
                                """

                        data = self.session.execute(sql)

                        for row in data:
                                # dict.append({'pidm':row.pidm, 'birim':row.birim, 'kurum':row.kurum,'timestamp':row.timestamp})
                                dict.append({'birim_pidm':row.birim_pidm ,'birim_name':row.birim_name})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response("NO DATA FOUND!")
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)


        def getPaylasilanKurumlar(self, birim_pidm):
                try:
                        dict = []

                        sql =  """
                                select k.pidm kurum_pidm, k.name kurum_name
                                from ss_kurumlar ss, kurumlar k
                                where ss.kurum_pidm = k.pidm and
                                ss.birim_pidm=%s
                                """%(birim_pidm)

                        data = self.session.execute(sql)

                        for row in data:
                                # dict.append({'pidm':row.pidm, 'birim':row.birim, 'kurum':row.kurum,'timestamp':row.timestamp})
                                dict.append({'kurum_pidm':row.kurum_pidm, 'kurum_name':row.kurum_name})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response("NO DATA FOUND!")
                        else:
                                return _json

                except Exception as e:
                        return Response("DB SQL Exception! ",e)



def getSurecSahipleri():
    cc = SSKurumlarClass()
    return cc.getSurecSahipleri()

def getPaylasilanKurumlar(birim_pidm):
    cc = SSKurumlarClass()
    return cc.getPaylasilanKurumlar(birim_pidm)

