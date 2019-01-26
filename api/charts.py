from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from sqlalchemy.inspection import inspect
from array import array
from db.model import *
import json


class Chart ():
        def __init__(self):
                self.conn = Connect()
                self.session = self.conn.session()

        def __del__(self):
                self.session.close()

        # GET query results
        def chart(self, model, params):
                try:
                        cid_ = params.get('cid')

                        data = self.session.query(model).filter_by(cid=cid_).limit(10).all()

                        dict = []
                        for key in data:
                                row = {}
                                row["name"]=key.name
                                row["value"]=key.value
                                dict.append(row)

                        _json = jsonify(dict)


                        if (len(dict) == 0):
                                return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                        else:
                                return _json

                except Exception as err:
                        return Response("!!! Chart Data Query Failure !!!", err)
        def treeKV (self, model, params):
                try:
                        cid_ = params.get('cid')

                        result = self.session.query(model).filter_by(cid=cid_)

                        dict = {"name":"Kurum"}
                        children1 = []
                        for key in result:
                                row = {"name":key.name}
                                children2 = []

                                data = key.data

                                for item in data:
                                        children2.append({"name":item,"value":item})

                                row["children"] = children2

                                children1.append(row)

                        dict["children"]=children1

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json


                except  Exception as err:
                        return Response("!!! Chart Data Query Failure !!!", err)

        def mapKV (self, model, params):
                try:
                        # cid_ = params.get('cid')
                        # data = self.session.query(model).filter_by(cid=cid_)

                        result = self.session.query(model).all()

                        dict = []
                        for key in result:
                                data = key.data
                                row = {"name":data["name"], "value":data["value"], "maxvalue":data["maxvalue"]}
                                dict.append(row)

                        # print(dict)

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json


                except  Exception as err:
                        return Response("!!! Chart World eMAP Data Query Failure !!!", err)


def chartsAction(id, params):
        cc = Chart()
        if (id == "01"):
                return cc.chart(ModelChartMaxKV,  params)
        elif (id == "02"):
                return cc.chart(ModelChartMaxKurumlar,  params)
        elif (id == "03"):
                return cc.chart(ModelChartMaxProfiller,  params)
        elif (id == "04"):
                return cc.chart(ModelChartMaxSurecler,  params)
        elif (id == "05"):
                return cc.chart(ModelChartTalepler,  params)
        elif (id == "06"):
                return cc.treeKV(ModelChartTreeBirimKV,params)
        elif (id == "07"):
                return cc.treeKV(ModelChartTreeProfilKV,params)
        elif (id == "08"):
                return cc.treeKV(ModelChartTreeBirimKurum,params)
        elif (id == "09"):
                return cc.mapKV(ModelChartMap,params)
        else:
                return Response('CHART ID FOR MODEL NOT FOUND!')

