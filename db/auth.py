from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean, JSON)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify
from flask import Response
from flask import request
from db.connection import Connect
import json
from array import array
from db.model import AuthModel, AuthLoginModel
import jwt
from db.config import ConfigJWT

class Auth():
    def __init__(self):
                self.conn = Connect()
                self.session = self.conn.session()

    def __del__(self):
                self.session.close()

    def getCids(self, uid):
        try:
                model = AuthModel
                data = self.session.query(model).filter_by(uid=uid)
                data = data.order_by(model.cid_name)

                dict = []
                for row in data:
                        dict.append( {'cid': row.cid, 'name': row.cid_name} )

                # print('dict: ', dict)
                _json = jsonify(dict)

                print('dict: ', dict)

                if (len(dict) == 0):
                        return Response([])
                else:
                        return _json

        except Exception as err:
                return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)

    def login(self, uid, pwd):
          try:

                model = AuthLoginModel
                data = self.session.query(model).filter_by(uid=uid, pwd=pwd)

                dict = []

                # JWT Token
                for row in data:
                        payload = { "uid": row.uid, "admin": "false"}
                        secretKey = ConfigJWT.SECRETKEY
                        signature = jwt.encode(payload, secretKey, algorithm='HS256').decode('utf-8')
                        dict.append( {'token': signature} )

                _json = jsonify(dict)

                if (len(dict) == 0):
                        return Response([])
                else:
                        return _json

          except Exception as err:
                return Response("*** Error! *** Login Exception!! ", err)


def getCids(uid):
    cc = Auth()
    return cc.getCids(uid)

def login(uid, pwd):
    cc = Auth()
    return cc.login(uid, pwd)