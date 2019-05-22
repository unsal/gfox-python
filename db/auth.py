from flask import jsonify
from flask import Response
from db.connection import Connect
from db.model import ModelAuth, ModelViewAuth, ModelCid
import jwt
import json
import datetime

from db.config import ConfigJWT


class Auth():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    def isAdmin(self, uid):
        try:
            admin = False
            data = self.session.query(ModelAuth).filter_by(uid=uid).limit(1)
            for row in data:
                admin = row.admin

            return admin

        except Exception as err:
            return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)

    def getCids(self, uid):
        try:
            dict = []
            if self.isAdmin(uid):
                model = ModelCid
                data = self.session.query(model).filter().order_by(model.name)
                for row in data:
                    dict.append({'cid': row.pidm, 'name': row.name})
            else:
                model = ModelViewAuth
                data = self.session.query(model).filter_by(username=uid).order_by(model.cid_name)
                for row in data:
                    dict.append({'cid': row.cid, 'name': row.cid_name})

            _json = jsonify(dict)

            # print('dict: ', dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)

    def login(self, params):
        try:

            username = params.get("username")
            password = params.get("password")

            query = {"username": username, "password": password, "enabled": True}
            data = self.session.query(ModelAuth).filter_by(**query).limit(1)

            print("username: ", username)

            dict = []

            # JWT Token
            for row in data:
                # key = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  # unique key, her seferinde farklı token üretmesi için
                exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)  # 8 saat expiration koyduk...
                payload = {"uid": row.username, "dpo": row.dpo, "admin": row.admin, "exp": exp}
                secretKey = ConfigJWT.SECRETKEY
                #  imza yaratılıyor... 3 parçadan oluşuyor.. xxxxx.yyyy.zzzzz -> yyyy kısmı payload cryptolu değil...
                #  zzzz kısmı xxxxx ve yyyyy nin karışımından üretilen  token kısmı...
                #  client tarafında bunu kontrol edebilirsin..
                token = jwt.encode(payload, secretKey, algorithm='HS256').decode('utf-8')

                dict.append({'token': token})
                print('token created succesfully...')

            _json = jsonify(dict)

            if (len(dict) == 0):
                print("Autherization failed...")
            else:
                print("Autherization successfully...", _json)

            return _json   # veya Response([]) boş dönmek için

        except Exception as err:
            return Response("*** Error! *** Login Exception!! ", err)

    def getAccounts(self, params):
        try:
            dict = []

            model = ModelViewAuth
            query = {"cid": params.get('cid')}
            data = self.session.query(model).filter_by(**query).order_by(model.username)

            for row in data:
                dict.append({'rownumber': row.rownumber, 'pidm': row.pidm, 'username': row.username, 'password': row.password, 'admin': row.admin, 'dpo': row.dpo, 'enabled': row.enabled})

            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)

    def update(self, params):
        try:
            cid = params.get('cid')
            uid = params.get('uid')
            pidm = params.get('pidm')
            username = params.get('username')
            password = params.get('password')
            enabled = params.get('enabled')

            query = {"pidm": pidm}
            data = self.session.query(ModelAuth).filter_by(**query)

            values = {"username": username, "password": password, "enabled": enabled, "uid": uid}
            data.update(values)

            self.session.commit()
            print("*** UPDATE successfully ***")
            return '', 204

        except Exception as err:
            print("!!! AUTH UPDATE error !!! ", err)
            return '', 404

    def add(self, params):
        try:

            cid_data = params.get('cid_data')
            uid = params.get('uid')
            username = params.get('username')
            password = params.get('password')
            enabled = params.get('enabled')

            data = {"username": username, "password": password, "enabled": enabled, "cid_data": cid_data, "uid": uid}

            print('data: ', data)

            # tek satır kayıt json datası oluştur {...}
            record = []
            record.append(data)

            print('record:', record)

            for row in record:
                self.session.add(ModelAuth(**row))

            self.session.commit()
            print("*** ADD successfully ***")
            return '', 204

        except Exception as err:
            print("!!! AUTH ADD error !!! ", err)
            return '', 404

    def delete(self, params):
        try:
            pidm = params.get('pidm')
            query = {"pidm": pidm}

            row = self.session.query(ModelAuth).filter_by(
                pidm=pidm).one()
            self.session.delete(row)
            self.session.commit()
            print("*** AUTH Record DELETED successfully ***")
            return '', 204
        except Exception as err:
            print("!!! ERROR ON DELETE !!! ", err)
            return '', 404

def getCids(uid):
    cc = Auth()
    return cc.getCids(uid)


def login(params):
    cc = Auth()
    return cc.login(params)

def actionAccounts(params):
    cc = Auth()
    type = params.get("type")
    if (type == "get"):
        return cc.getAccounts(params)
    elif (type == "update"):
        return cc.update(params)
    elif (type == "add"):
        return cc.add(params)
    elif (type == "delete"):
        return cc.delete(params)
    else:
        return '', 404
