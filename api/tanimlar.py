from flask import Response
from flask import jsonify
from db.connection import Connect
from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Ortamlar, Sureler, Kurumlar,Dayanaklar, PaylasimAmaclari, PaylasimSekilleri, Ulkeler

class GetTanimlar():
    def __init__(self, modelClass):
        self.conn = Connect()
        self.session = self.conn.session()
        self.model = modelClass   # !!!modelClass() parentezle yaparsan class create edilir, bu koşulda olmaz...

    def __del__(self):
        self.session.close()

    def message(self):
        try:
            dict = []

            if (self.model == Sistemler):
                data = self.session.query(self.model.id, self.model.name, self.model.type, self.model.timestamp)
            elif (self.model == Ulkeler):
                data = self.session.query(self.model.id, self.model.name, self.model.phone_area,self.model.secure, self.model.timestamp)
            else:
                data = self.session.query(self.model.id, self.model.name, self.model.timestamp)

            data = data.order_by(self.model.name)

            for row in data:

                if (self.model == Sistemler):
                    dict.append({'id':row.id, 'name':row.name,'type':row.type, 'timestamp':row.timestamp})
                elif (self.model == Ulkeler):
                    dict.append({'id':row.id, 'name':row.name,'phone_area':row.phone_area,'secure':row.secure, 'timestamp':row.timestamp})
                else:
                    dict.append({'id':row.id, 'name':row.name,'timestamp':row.timestamp})

            # _json = jsonify({"Tanimlar":dict})
            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response("NO DATA found!")
            else:
                return _json

        except Exception as e:
            return Response("sa query error! ",e)


def message(id):
    if (id == "profiller"):
            t = GetTanimlar(Profiller)
            return t.message()
    elif (id=="birimler"):
            t = GetTanimlar(Birimler)
            return t.message()
    elif (id=="dayanaklar"):
            t = GetTanimlar(Dayanaklar)
            return t.message()
    elif (id=="dokumanlar"):
            t = GetTanimlar(Dokumanlar)
            return t.message()
    elif (id=="islemeamaclari"):
            t = GetTanimlar(IslemeAmaclari)
            return t.message()
    elif (id=="kanallar"):
            t = GetTanimlar(Kanallar)
            return t.message()
    elif (id=="kv"):
            t = GetTanimlar(KV)
            return t.message()
    elif (id=="ortamlar"):
            t = GetTanimlar(Ortamlar)
            return t.message()
    elif (id=="sistemler"):
            t = GetTanimlar(Sistemler)
            return t.message()
    elif (id=="sureler"):
            t = GetTanimlar(Sureler)
            return t.message()
    elif (id=="kurumlar"):
            t = GetTanimlar(Kurumlar)
            return t.message()
    elif (id=="paylasimamaclari"):
            t = GetTanimlar(PaylasimAmaclari)
            return t.message()
    elif (id=="paylasimsekilleri"):
            t = GetTanimlar(PaylasimSekilleri)
            return t.message()
    elif (id=="ulkeler"):
            t = GetTanimlar(Ulkeler)
            return t.message()
    else:
            return "Geçersiz Tanım"


# if __name__ == "__main__":
#     e = TanimlarApi()
#     e.message()

    # print("Base created successfully..")