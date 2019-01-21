# - *- coding: utf- 8 - *-
from flask import Flask, jsonify
from flask import request
import json

# API
from db.auth import getCids, login
from api.export import downloadExcel

from db.model import *
from api.framework import *
from api.charts import *

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


#************** options  **************************
@app.route('/options/<id>', methods=['POST'])
def returnOptions(id):
    params = request.get_json(silent=True)
    model = getOptionsModel(id)
    return optionsAction(model,params)


#************** TANIMLAR  **************************
@app.route('/tanimlar/<id>/<type>', methods=['POST'])
def returnTanimlar(id, type):
    params = request.get_json(silent=True)
    model = getModel(id)
    return myAction(model, model, params, type) #id: get, add, update, delete

#************** TANIMLAR DIGER  **************************
@app.route('/bolumler/<type>', methods=['POST'])
def returnTanimlarBolumler(type):
    params = request.get_json(silent=True)
    return myAction(ModelBolumler, ModelViewBolumler, params, type) #id: get, add, update, delete

@app.route('/surecler/<type>', methods=['POST'])
def returnTanimlarSurecler(type):
    params = request.get_json(silent=True)
    return myAction(ModelSurecler, ModelViewSurecler, params, type) #id: get, add, update, delete

@app.route('/anaveriler/<type>', methods=['POST'])
def returnAnaveriler(type):
    params = request.get_json(silent=True)
    return myAction(ModelAnaveriler, ModelViewAnaveriler, params, type) #id: get, add, update, delete

@app.route('/aktarimlar/<type>', methods=['POST'])
def returnAktarimlar(type):
    params = request.get_json(silent=True)
    return myAction(ModelAktarimlar, ModelViewAktarimlar, params, type) #id: get, add, update, delete

@app.route('/talepler/<type>', methods=['POST'])
def returnTalepler(type):
    params = request.get_json(silent=True)
    return myAction(ModelTalepler, ModelViewTalepler, params, type) #id: get, add, update, delete

@app.route('/kv/<type>', methods=['POST'])
def returnKV(type):
    params = request.get_json(silent=True)
    return myAction(ModelKV, ModelViewKV, params, type) #id: get, add, update, delete

@app.route('/ulkeler/<type>', methods=['POST'])
def returnUlkeler(type):
    params = request.get_json(silent=True)
    return myAction(ModelUlkeler, ModelViewUlkeler, params, type) #id: get, add, update, delete

@app.route('/sistemler/<type>', methods=['POST'])
def returnSistemler(type):
    params = request.get_json(silent=True)
    return myAction(ModelSistemler, ModelViewSistemler, params, type) #id: get, add, update, delete

@app.route('/sorumlular/<type>', methods=['POST'])
def returnSorumlular(type):
    params = request.get_json(silent=True)
    return myAction(ModelSorumlular, ModelSorumlular, params, type) #id: get, add, update, delete

@app.route('/birimler/<type>', methods=['POST'])
def returnBirimler(type):
    params = request.get_json(silent=True)
    return myAction(ModelBirimler, ModelViewBirimler, params, type) #id: get, add, update, delete

# ****************** CHARTS ************************************************
@app.route('/chart/<id>', methods=['POST'])
def returnChart(id):
    params = request.get_json(silent=True)
    return chartsAction(id,  params)

# ****************** MAIN ************************************************
if __name__=="__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True, threaded=True)
    app.run(host="127.0.0.1", port=8000, debug=True)
    print("Server started successfully..")

# concurrent requestler için:
        # app.debug = True
        # return_server = WSGIServer(('', 8000), app)
        # return_server.serve_forever()













