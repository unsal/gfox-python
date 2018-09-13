from flask import Flask, request
from api.tanimlar import getTanim, addTanim, delTanim
from api.ss import ssMessage
from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Ortamlar, Sureler, Kurumlar,Dayanaklar, PaylasimAmaclari, PaylasimSekilleri, Ulkeler

from flask_cors import CORS

app = Flask(__name__)

# TR karakterler \n\bbn\a vb. ascii olarak basmaası iin
app.config['JSON_AS_ASCII'] = False

# React tarafında Access-Control-Allow-Origin hatasını önlemek için
CORS(app)

# app.config.from_object('config.Config')

@app.route('/')
def root():
    return 'Python web server working successfully...'

# Profiller
# @app.route('/profiller', methods=['GET'])
# def getProfiller():
#     api = GetTanimlar(Profiller)
#     return api.message()


# GET TANIM
@app.route('/tanimlar/<id>', methods=['GET'])
def get(id):
    return getTanim(id)

# ADD TANIM
@app.route('/tanimlar/add', methods=['POST'])
def add():
    _form = request.form
    return addTanim(_form)


# DELETE TANIM
@app.route('/tanimlar/del', methods=['POST'])
def delete():
    _form = request.form
    return delTanim(_form)

# Süreç Sahibi
@app.route('/ss/<id>', methods=['GET'])
def getSS(id):
    return ssMessage(id)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=2300, debug=True)
    print("Server started successfully..")



