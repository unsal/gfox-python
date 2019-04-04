from flask import jsonify
from flask import Response
from db.connection import Connect
from db.model import ModelAuth, ModelViewAuth, ModelCid
import jwt
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
                data = self.session.query(ModelViewAuth).filter_by(username=uid).order_by(model.cid_name)
                for row in data:
                    dict.append({'cid': row.cid, 'name': row.cid_name})

            # print('dict: ', dict) ..
            _json = jsonify(dict)

            # print('dict: ', dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)

    def login(self, username, password):
        try:

            params = {"username": username, "password": password, "enabled": True}
            data = self.session.query(ModelAuth).filter_by(**params).limit(1)

            dict = []

            # JWT Token
            for row in data:
                payload = {"uid": row.username}
                secretKey = ConfigJWT.SECRETKEY
                signature = jwt.encode(
                    payload, secretKey, algorithm='HS256').decode('utf-8')
                dict.append({'token': signature, "uid": row.username, "dpo": row.dpo, "admin": row.admin})
                print('token created succesfully...')

            _json = jsonify(dict)

            if (len(dict) == 0):
                print("Autherization failed...")
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("*** Error! *** Login Exception!! ", err)

    def getAccounts(self, params):
        try:
            dict = []

            model = ModelViewAuth
            query = {"cid": params.get('cid')}
            data = self.session.query(model).filter_by(**query).order_by(model.username)

            for row in data:
                dict.append({'username': row.username, 'password': row.password, 'admin': row.admin, 'dpo': row.dpo, 'enabled': row.enabled})

            print('dict: ', dict)

            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)


def getCids(uid):
    cc = Auth()
    return cc.getCids(uid)


def login(username, password):
    cc = Auth()
    return cc.login(username, password)

def actionAccounts(params, type):
    cc = Auth()
    if (type == "get"):
        return cc.getAccounts(params)
    # elif (type == "add"):
    #     return cc.add(baseModel, params)
    # elif (type == "update"):
    #     return cc.update(baseModel, params)
    # elif (type == "delete"):
    #     return cc.delete(baseModel, params)
    else:
        return '', 404
