from flask import Response
from flask import jsonify
from db.connection import Connect
from db.model import Profiller


class GetProfiller():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    def message(self):
        try:
            dict = []

            data = self.session.query(Profiller.id, Profiller.name, Profiller.timestamp)
            data = data.order_by(Profiller.name)

            for row in data:
                dict.append({'id':row.id, 'name':row.name,'timestamp':row.timestamp})

            # _json = jsonify({"Profiller":dict})
            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response("NO DATA found!")
            else:
                return _json

        except Exception as e:
            return Response("sa query error! ",e)



class AddProfil():
    def __init__(self, name):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    def message(self):
        try:
            dict = []

            data = self.session.query(Profiller.id, Profiller.name, Profiller.timestamp)
            data = data.order_by(Profiller.name)

            for row in data:
                dict.append({'id':row.id, 'name':row.name,'timestamp':row.timestamp})

            # _json = jsonify({"Profiller":dict})
            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response("NO DATA found!")
            else:
                return _json

        except Exception as e:
            return Response("sa query error! ",e)

# if __name__ == "__main__":
#     e = ProfillerApi()
#     e.message()

    # print("Base created successfully..")