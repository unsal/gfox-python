from flask import Flask
from api.profiller import ProfillerApi
from api.birimler import BirimlerApi
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
    api = ProfillerApi()
    return api.message()

# Birimler
@app.route('/birimler', methods=['GET'])
def getBirimler():
    api = BirimlerApi()
    return api.message()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=2300, debug=True)
    print("Server started successfully..")






