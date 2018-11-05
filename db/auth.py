from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean, JSON)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify
from flask import Response
from flask import request
from db.connection import Connect
import json
from array import array
from db.model import ViewAuthModel


class ViewAuth():
    def __init__(self, uid):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model =  ViewAuthModel
                self.model.uid = uid

    def __del__(self):
                self.session.close()

    def getCids(self):
        try:
                data = self.session.query( self.model.cid, self.model.cid_name).filter_by(uid=self.model.uid)
                data = data.order_by(self.model.cid_name)

                dict = []
                for row in data:
                        dict.append( {'cid': row.cid, 'name': row.cid_name} )

                _json = jsonify(dict)

                if (len(dict) == 0):
                        return Response([])
                else:
                        return _json

        except Exception as err:
                return Response("*** Error! *** ViewAuth->getCids Exception!! ", err)

def getCids(uid):
    cc = ViewAuth(uid)
    return cc.getCids()