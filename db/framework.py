from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
import json
from array import array
from sqlalchemy.inspection import inspect
from db.model import *


class Framework ():
        def __init__(self):
                self.conn = Connect()
                self.session = self.conn.session()

        def __del__(self):
                self.session.close()

        # GET query results
        def get(self, model, params):
                try:
                        cid_ = params.get('cid')

                        data = self.session.query(model).filter_by(cid=cid_)

                        dict = []
                        for row in data:
                                myRow = {}
                                instance = inspect(row)
                                for key, item in instance.attrs.items():

                                        isDataField = "_data" in key
                                        isExcludedField = (key in ['cid', 'uid', 'timestamp'])

                                        if isDataField:
                                           tableName = key.replace('_data','')
                                           myRow[key]=self.createDict(tableName, item.value, cid_)
                                        elif not isExcludedField:
                                           myRow[key]=item.value

                                dict.append(myRow)

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("!!! Get Query ERROR !!!", err)


        def add(self, model, params):
                try:

                        data = []
                        data.append(params)

                        for row in data:
                                self.session.add(model(**row))

                        self.session.commit()

                        print("*** Record ADD successfully *** ")
                        return '', 204
                except Exception as err:
                        print("!!! Record ADD ERROR !!! ", err)
                        return '', 404


        def update(self, model, params):
                try:
                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')
                        row = self.session.query(model).filter_by( pidm=pidm_, cid=cid_)

                        row.update(params)

                        self.session.commit()
                        print("*** UPDATE successfully ***")
                        return '', 204
                except Exception as err:
                        print("!!! UPDATE error !!! ", err)
                        return '', 404


        def delete(self, model, params):
                try:

                        pidm_ = params.get('pidm')
                        cid_ = params.get('cid')

                        row = self.session.query(model).filter_by( pidm=pidm_, cid=cid_).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("*** Record DELETE successfully ***")
                        return '', 204
                except Exception as err:
                        print("!!! Record DELETE ERROR !!! ", err)
                        return '', 404

        # verbis > ekranlarında multiple veriye sahip hücrelere kaynaktan dönen pidmları [{pidm, name}] olarak dönmek için
        def createDict( self, tableName, data, cid ):
        #create dict[pidm, name] from data[pidm]
                try:
                        dict = []
                        items = array('i', data) #array as integer 'i'

                        for item in items:
                                table_pidm = item
                                table_name = self.getPidmName(tableName, table_pidm ,cid)
                                dict.append({'pidm':table_pidm, 'name':table_name})

                        if (len(dict) == 0):
                                return []
                        else:
                                return dict

                except Exception:
                        return []


          # for converting json pidm -> names
        def getPidmName(self, tableName, pidm, cid):
                try:
                        sql =  """
                                select  {0}.name
                                from    {0}
                                where   {0}.pidm={1} and {0}.cid={2}
                                limit 1
                                """.format(tableName, pidm, cid)

                        data = self.session.execute(sql)
                        name = ""
                        for row in data:
                                name = row.name
                        return name

                except Exception:
                        return "Error!"

        #dropdown için..
        def getOptions(self, model, params):
                try:
                        cid_ = params.get('cid')

                        data = self.session.query(model).filter_by(cid=cid_)

                        dict = []
                        for row in data:
                               dict.append({'pidm': row.pidm, 'name': row.name, 'pidm':row.pidm})

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("!!! Get Options ERROR !!!", err)


def myAction(baseModel, viewModel, params, type):
        cc = Framework()
        if (type=="get"):
                return cc.get(viewModel, params)
        elif (type=="add"):
                return cc.add(baseModel, params)
        elif (type=="update"):
                return cc.update(baseModel, params)
        elif (type=="delete"):
                return cc.delete(baseModel, params)
        else:
                return '', 404


def optionsAction(model, params):
        cc = Framework()
        return cc.getOptions(model,params)