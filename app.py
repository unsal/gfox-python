from flask import Flask
from api.profiller import ProfillerApi
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

# Tüm profilleri getir
@app.route('/profiller', methods=['GET'])
def getMessage():
    api = ProfillerApi()
    return api.message()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=2300, debug=True)
    print("Server started successfully..")






