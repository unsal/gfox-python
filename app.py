from flask import Flask
from api.tanimlar import GetTanimlar, message
from db.model import Profiller, Birimler, KV, IslemeAmaclari, Kanallar, Sistemler, Dokumanlar, Dayanaklar, Ortamlar, Sureler

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
# @app.route('/profiller', methods=['GET'])
# def getProfiller():
#     api = GetTanimlar(Profiller)
#     return api.message()

# Tanımlar
@app.route('/tanimlar/<id>', methods=['GET'])
def getTanimlar(id):
    return message(id)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=2300, debug=True)
    print("Server started successfully..")



