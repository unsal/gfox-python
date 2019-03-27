#!/usr/bin/env python3
# - *- coding: utf- 8 - *-

from flask import Flask
from flask import request
# import json

# API
from db.auth import getCids, login
# from api.export import downloadExcel

from db.model import *
from api.frameworkTanimlar import *
from api.frameworkEnvanter import *
from api.analiz.charts import *

from flask_cors import CORS

# concurrent requestler için en altta main de
# from gevent.pywsgi import WSGIServer
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
    uid = data.get('uid')
    response = getCids(uid)
    return response


@app.route('/auth/login', methods=['POST'])
def _login():
    data = request.get_json(silent=True)
    uid = data.get("uid")
    pwd = data.get("pwd")
    response = login(uid, pwd)

    return response

# ****************** EXCEL ************************************************


# @app.route('/download', methods=['POST'])
# def _export():
#     data = request.get_json(silent=True)
#     cid = data.get('cid')
#     response = downloadExcel(cid)
#     return response


# ************** options  **************************
@app.route('/options/<id>', methods=['POST'])
def returnOptions(id):
    params = request.get_json(silent=True)
    model = getOptionsModel(id)
    return optionsAction(model, params)


# ************** TANIMLAR  **************************
@app.route('/tanimlar/<id>/<type>', methods=['POST'])
def returnTanimlar(id, type):
    params = request.get_json(silent=True)
    model = getModel(id)
    return myAction(model, model, params, type)

# ************** TANIMLAR DIGER  **************************


@app.route('/bolumler/<type>', methods=['POST'])
def returnTanimlarBolumler(type):
    params = request.get_json(silent=True)
    return myAction(ModelBolumler, ModelViewBolumler, params, type)


@app.route('/surecler/<type>', methods=['POST'])
def returnTanimlarSurecler(type):
    params = request.get_json(silent=True)
    return myAction(ModelSurecler, ModelViewSurecler, params, type)


@app.route('/talepler/<type>', methods=['POST'])
def returnTalepler(type):
    params = request.get_json(silent=True)
    return myAction(ModelTalepler, ModelViewTalepler, params, type)


@app.route('/kv/<type>', methods=['POST'])
def returnKV(type):
    params = request.get_json(silent=True)
    return myAction(ModelKV, ModelViewKV, params, type)


@app.route('/ulkeler/<type>', methods=['POST'])
def returnUlkeler(type):
    params = request.get_json(silent=True)
    return myAction(ModelUlkeler, ModelViewUlkeler, params, type)


@app.route('/sistemler/<type>', methods=['POST'])
def returnSistemler(type):
    params = request.get_json(silent=True)
    return myAction(ModelSistemler, ModelViewSistemler, params, type)


@app.route('/sorumlular/<type>', methods=['POST'])
def returnSorumlular(type):
    params = request.get_json(silent=True)
    return myAction(ModelSorumlular, ModelSorumlular, params, type)


@app.route('/birimler/<type>', methods=['POST'])
def returnBirimler(type):
    params = request.get_json(silent=True)
    return myAction(ModelBirimler, ModelViewBirimler, params, type)


@app.route('/kisiler/<type>', methods=['POST'])
def returnKisiler(type):
    params = request.get_json(silent=True)
    return myAction(ModelKisiler, ModelKisiler, params, type)

# ****************** CHARTS ************************************************


@app.route('/chart', methods=['POST'])
def returnChart():
    params = request.get_json(silent=True)
    return getChartData(params)


# ****************** ANAVERILER && AKTARIMLAR ************************************************
# id: anaveriler, aktarimlar / type: get, update, delete
@app.route('/envanter/<id>/<type>', methods=['POST'])
def returnEnvanter(id, type):
    params = request.get_json(silent=True)
    return actionEnvanter(params, id, type)


# ****************** MAIN ************************************************
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True, threaded=True)
    # app.run(host="0.0.0.0",debug=True) # server
    print("Server started successfully..")

# concurrent requestler için:
    # app.debug = True
    # return_server = WSGIServer(('', 8000), app)
    # return_server.serve_forever()
