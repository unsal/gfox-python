# - *- coding: utf- 8 - *-
from flask import Flask, jsonify
from flask import request
import json

# API
from api.tanimlar.tanimlar import getTanim, addTanim, deleteTanim, getNextPidm
from api.ss.ssdokumanlar import getSSDokumanlar, addSSDokuman, delSSDokuman
from api.ss.sscommon import getSSCommon, deleteSSCommon, addSSCommon
from api.verbis.kvprofil import get_kvprofil, add_kvprofil, update_kvprofil, delete_kvprofil
from api.verbis.kvpaylasim import get_kvpaylasim, add_kvpaylasim, update_kvpaylasim, delete_kvpaylasim
from api.verbis.kvanaveri import get_kvanaveri, add_kvanaveri, delete_kvanaveri, update_kvanaveri
from api.verbis.kvtalepler import get_kvtalepler, add_kvtalepler
from db.auth import getCids, login
from api.export import downloadExcel
from api.tanimlar.bolumler import getBolumler, addBolum, deleteBolum

from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Ortamlar, Sureler, Kurumlar,Dayanaklar, PaylasimAmaclari, PaylasimSekilleri, Ulkeler

from flask_cors import CORS

#concurrent requestler için en altta main de
from gevent.pywsgi import WSGIServer
import logging
# logging.basicConfig()

app = Flask(__name__)

logger = logging.getLogger('gunicorn.error')


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
@app.route('/tanimlar/<id>', methods=['POST'])
def _getTanim(id):
        data = request.get_json(silent=True)
        cid  = data.get('cid')
        response = getTanim(id, cid)
        return response


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

# Get Next Pidm
@app.route('/tanimlar/pidm/<id>', methods=['GET'])
def _getNextPidm(id):
    data = getNextPidm(id)
    return data

# SS ******************************************************
# GET COMMON
@app.route('/ss/common/<id>', methods=['POST'])
def _getSSCommon(id):
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = getSSCommon(id, cid)
    return response

# DEL COMMON
@app.route('/ss/common/delete', methods=['POST'])
def _delSSCommon():
    _form = request.form
    response = deleteSSCommon(_form)
    return response

# ADD COMMON
@app.route('/ss/common/add', methods=['POST'])
def _addSSKurum():
    _form = request.form
    response = addSSCommon(_form)
    return response


# ************* GET SS DOKUMANLAR *******************
@app.route('/ss/dokumanlar', methods=['POST'])
def _getSSDokumanlar():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = getSSDokumanlar(cid)
    return response

# ADD SS DOKUMAN
@app.route('/ss/dokumanlar/add', methods=['POST'])
def _addSSDokuman():
    _form = request.form
    response = addSSDokuman(_form)
    return response

# DELETE SS DOKUMAN
@app.route('/ss/dokumanlar/del', methods=['POST'])
def _delSSDokuman():
    _form = request.form
    response = delSSDokuman(_form)
    return response


# ******************** VERBIS ************************************
#************** KV PROFIL **************************
@app.route('/verbis/kvprofil', methods=['POST'])
# KVProfil - GET
def _get_kvprofil():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = get_kvprofil(cid)
    return response

@app.route('/verbis/kvprofil/add', methods=['POST'])
# KVProfil - ADD
def _add_kvprofil():
    data = request.get_json(silent=True)
    response = add_kvprofil(data) #data=>full json kvprofil datasıdır
    return response

@app.route('/verbis/kvprofil/update', methods=['POST'])
# KVProfil - UPDATE
def _update_kvprofil():
    data = request.get_json(silent=True)
    response = update_kvprofil(data) #data=>full json kvprofil datasıdır
    return response

@app.route('/verbis/kvprofil/delete', methods=['POST'])
# KVProfil - DELETE
def _delete_kvprofil():
    data = request.get_json(silent=True)
    response = delete_kvprofil(data) #data=>full json kvprofil datasıdır
    return response

# ****************** KVPAYLASIM ************************************************
@app.route('/verbis/kvpaylasim', methods=['POST'])
# GET
def _get_kvpaylasim():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = get_kvpaylasim(cid)
    return response

@app.route('/verbis/kvpaylasim/add', methods=['POST'])
# ADD
def _add_kvpaylasim():
    data = request.get_json(silent=True)
    response = add_kvpaylasim(data)
    return response

@app.route('/verbis/kvpaylasim/update/<id>', methods=['POST'])
# UPDATE & DELETE DATACELL
def _update_kvpaylasim(id):
    data = request.get_json(silent=True)
    response = update_kvpaylasim(id, data)
    return response

@app.route('/verbis/kvpaylasim/delete', methods=['POST'])
# DELETE ROW
def _delete_kvpaylasim():
    data = request.get_json(silent=True)
    response = delete_kvpaylasim(data) # [{pidm}]
    return response

# ****************** KVANAVERI ************************************************
@app.route('/verbis/kvanaveri', methods=['POST'])
# GET
def _get_kvanaveri():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = get_kvanaveri(cid)
    return response

@app.route('/verbis/kvanaveri/add', methods=['POST'])
# ADD
def _add_kvanaveri():
    data = request.get_json(silent=True)
    response = add_kvanaveri(data)
    return response

@app.route('/verbis/kvanaveri/delete', methods=['POST'])
# DELETE ENTIRE ROW
def _delete_kvanaveri():
    data = request.get_json(silent=True)
    response = delete_kvanaveri(data) # [{pidm}]
    return response

@app.route('/verbis/kvanaveri/update/<id>', methods=['POST'])
# UPDATE & DELETE DATACELL
def _update_kvanaveri(id):
    data = request.get_json(silent=True)
    response = update_kvanaveri(id, data)
    return response


# ****************** MAIN ************************************************
@app.route('/verbis/kvtalepler', methods=['GET'])
# GET
def _get_kvtalepler():
    response = get_kvtalepler()
    return response

@app.route('/verbis/kvtalepler/add', methods=['POST'])
# ADD
def _add_kvtalepler():
    data = request.get_json(silent=True)
    response = add_kvtalepler(data)
    return response


# ****************** AUTH ************************************************
@app.route('/auth/cids', methods=['POST'])
# GET
def _getCids():
    data = request.get_json(silent=True)
    uid  = data.get('uid')
    response = getCids(uid)
    return response

@app.route('/auth/login', methods=['POST'])
def _login():
    data = request.get_json(silent=True)
    uid  = data.get('uid')
    pwd  = data.get('pwd')
#     logger.info('uid: '+uid)
    response = login(uid, pwd)

    return response

# ****************** EXCEL ************************************************
@app.route('/download', methods=['POST'])
def _export():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = downloadExcel(cid)
    return response

#************** BOLUMLER **************************
@app.route('/tanimlar/bolumler', methods=['POST'])
def _getBolumler():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = getBolumler(cid)
    return response

# ADD
@app.route('/tanimlar/bolumler/add', methods=['POST'])
def _addBolumler():
    data = request.get_json(silent=True)
    response = addBolum(data)
    return response

# DEL
@app.route('/tanimlar/bolumler/delete', methods=['POST'])
def _deleteBolum():
    data = request.get_json(silent=True)
    response = deleteBolum(data)
    return response



# ****************** MAIN ************************************************
if __name__=="__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True, threaded=True)
    app.run(host="127.0.0.1", port=8000, debug=True)
    print("Server started successfully..")

# concurrent requestler için:
        # app.debug = True
        # http_server = WSGIServer(('', 8000), app)
        # http_server.serve_forever()













