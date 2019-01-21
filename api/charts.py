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
        def chartData(self, model, params):
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


def chartsAction(id, params):
        cc = Chart()
        if (id == "01"):
                return cc.chartData(ModelChartMaxKV,  params)
        elif (id == "02"):
                return cc.chartData(ModelChartMaxKurumlar,  params)
        elif (id == "03"):
                return cc.chartData(ModelChartMaxProfiller,  params)
        elif (id == "04"):
                return cc.chartData(ModelChartMaxSurecler,  params)
        elif (id == "05"):
                return cc.chartData(ModelChartTalepler,  params)
        else:
                return Response('CHART ID FOR MODEL NOT FOUND!')
