from flask import Flask
from api.profiller import GetProfiller
from api.birimler import GetBirimler
from api.kv import GetKV
from api.islemeAmaclari import GetIslemeAmaclari
from api.toplamaKanallari import GetToplamaKanallari
from flask_cors import CORS

app = Flask(__name__)

#TR karakterler \n\bbn\a vb. ascii olarak basmaası için
app.config['JSON_AS_ASCII'] = False

# React tarafında Access-Control-Allow-Origin hatasını önlemek için
CORS(app)

# app.config.from_object('config.Config')

@app.route('/')
def root():
    return 'Python web server working successfully...'

# Profiller
@app.route('/profiller', methods=['GET'])
def getProfiller():
    api = GetProfiller()
    return api.message()

# Birimler
@app.route('/birimler', methods=['GET'])
def getBirimler():
    api = GetBirimler()
    return api.message()

# KV
@app.route('/kv', methods=['GET'])
def getKV():
    api = GetKV()
    return api.message()

# Islenme Amacı
@app.route('/islemeamaclari', methods=['GET'])
def getIslemeAmaclari():
    api = GetIslemeAmaclari()
    return api.message()

# Toplama Kanalları
@app.route('/toplamakanallari', methods=['GET'])
def getToplamaKanallari():
    api = GetToplamaKanallari()
    return api.message()



if __name__=="__main__":
    app.run(host="0.0.0.0", port=2300, debug=True)
    print("Server started successfully..")






