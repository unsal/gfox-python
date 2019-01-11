# - *- coding: utf- 8 - *-
from flask import Flask, jsonify
from flask import request
import json

# API
from api.tanimlar.tanimlar import *
from api.verbis.kvtalepler import *
from db.auth import getCids, login
from api.export import downloadExcel
from api.tanimlar.bolumler import *
from api.tanimlar.surecler import *

from api.verbis.anaveriler import *
from api.verbis.aktarimlar import *

from db.model import *

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

# Get Tanim Name for pidm. Anaveriler için
@app.route('/tanimlar/name', methods=['POST'])
def _getTanimName():
    data = request.get_json(silent=True)
    id  = data.get('id')
    pidm  = data.get('pidm')
    cid  = data.get('cid')

    response = getTanimName(id, pidm, cid)
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

#************** SURECLER **************************
@app.route('/tanimlar/surecler', methods=['POST'])
def _getSurecler():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = getSurecler(cid)
    return response

# 4dropdown
@app.route('/tanimlar/sureclerdd', methods=['POST'])
def _getSureclerDropdown():
    data = request.get_json(silent=True)
    cid  = data.get('cid')
    response = getDropdownSurecler(cid)
    return response

@app.route('/tanimlar/surecler/add', methods=['POST'])
def _addSurecler():
    data = request.get_json(silent=True)
    response = addSurec(data)
    return response

@app.route('/tanimlar/surecler/delete', methods=['POST'])
def _deleteSurec():
    data = request.get_json(silent=True)
    response = deleteSurec(data)
    return response


#************** ANAVERILER **************************
@app.route('/verbis/anaveriler/<type>', methods=['POST'])
def httpAnaveriler(type):
    params = request.get_json(silent=True)
    return anaverilerAction(type,params) #id: get, add, update, delete

#************** AKTARIMLAR **************************
@app.route('/verbis/aktarimlar/<type>', methods=['POST'])
def httpAktarimlar(type):
    params = request.get_json(silent=True)
    return aktarimlarAction(type,params) #id: get, add, update, delete


# ****************** MAIN ************************************************
if __name__=="__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True, threaded=True)
    app.run(host="127.0.0.1", port=8000, debug=True)
    print("Server started successfully..")

# concurrent requestler için:
        # app.debug = True
        # http_server = WSGIServer(('', 8000), app)
        # http_server.serve_forever()













