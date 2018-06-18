# Süreç Sahibi
from flask import Response
from flask import jsonify
from db.connection import Connect
from sqlalchemy.sql import text

class GetKurumlar():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    def message(self):
        try:
            dict = []

            sql =  """
                select ss.id, b.name birim, k.name kurum, ss.timestamp
                from ss_kurumlar ss, birimler b, kurumlar k
                where ss.birim_id = b.id and ss.kurum_id = k.id
                order by ss.id
                """

            data = self.session.execute(sql)

            for row in data:
                    dict.append({'id':row.id, 'birim':row.birim, 'kurum':row.kurum,'timestamp':row.timestamp})

            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response("NO DATA FOUND!")
            else:
                return _json

        except Exception as e:
            return Response("sa query error! ",e)


class GetDokumanlar():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    def message(self):
        try:
            dict = []

            sql =  """
                select ss.id, b.name birim, d.name dokuman, y.name yayin, ss.timestamp
                from ss_dokumanlar ss, birimler b, dokumanlar d, ss_yayindurumu y
                where ss.birim_id = b.id and ss.dokuman_id = d.id and ss.yayin_id = y.id
                order by ss.id
                """

            data = self.session.execute(sql)

            for row in data:
                    dict.append({'id':row.id, 'birim':row.birim, 'dokuman':row.dokuman,'yayin':row.yayin, 'timestamp':row.timestamp})

            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response("NO DATA FOUND!")
            else:
                return _json

        except Exception as e:
            return Response("sa query error! ",e)


def ssMessage(id):
        if (id == "kurumlar"):
            api = GetKurumlar()
            return api.message()
        elif (id=="kvdokumanlar"):
            api = GetDokumanlar()
            return api.message()
        else:
            return "Geçersiz Tanım"

