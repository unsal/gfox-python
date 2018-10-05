# - *- coding: utf- 8 - *-
from flask import Flask
from flask import request
# API
from api.tanimlar.tanimlar import getTanim, addTanim, deleteTanim, getNextPidm
from api.ss.sskurumlar import getSurecSahipleri, getPaylasilanKurumlar

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

# TANIMLAR **************************************
# GET TANIM
@app.route('/tanimlar/<id>', methods=['GET'])
def _getTanim(id):
    json = getTanim(id)
    return json

# ADD TANIM
@app.route('/tanimlar/add', methods=['POST'])
def _addTanim():
    _form = request.form
    response = addTanim(_form)
    return response


# DELETE TANIM
@app.route('/tanimlar/del', methods=['POST'])
def _deleteTanim():
    _form = request.form
    response = deleteTanim(_form)
    return response


# SS ******************************************************
# 1) iki bileşendir. önce süreç sahibi birimleri listelemek içindir.
@app.route('/ss/birimler', methods=['GET'])
def _getSurecSahipleri():
    json = getSurecSahipleri()
    return json
# 2) süreç sahibi birimlerin paylaşan kurumlarını listelemek için
@app.route('/ss/birimler/kurumlar/<id>', methods=['GET'])
def _getPaylasilanKurumlar(id):
    json = getPaylasilanKurumlar(id)
    return json

# Get Next Pidm
@app.route('/tanimlar/pidm/<id>', methods=['GET'])
def _getNextPidm(id):
    json = getNextPidm(id)
    return json

if __name__=="__main__":
    app.run(host="0.0.0.0", port=2300, debug=True)
    print("Server started successfully..")



