from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
from sqlalchemy.inspection import inspect
from array import array
from db.model import *
from api.gfox import *
import json


class Chart ():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    # GET query results

    def kvData(self, params):
        try:
            # params = {name:'xx', cid:'xx'} olduğu varsayılıyor
            # {name!r} => sonucu tırnaklı string olarak basmak için => " 'xx' "
            sql = " select * from f_chart_kv({name!r},{cid}) order by value desc limit 20".format(
                **params)

            result = self.session.execute(sql)

            dict = []
            for key in result:
                row = {}
                row["name"] = key.name
                row["value"] = key.value
                dict.append(row)

            _json = jsonify(dict)

            if (len(dict) == 0):
                # böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("!!! DBService getChartKV ERROR !!!", err)

    def barData(self, params):
        try:
            # params = {name:'xx', cid:'xx'} olduğu varsayılıyor
            # {name!r} => sonucu tırnaklı string olarak basmak için => " 'xx' "
            sql = " select * from f_chart_kv_bar({name!r},{cid}) ".format(
                **params)

            result = self.session.execute(sql)

            dict = []
            for key in result:
                row = {}
                row["name"] = key.name
                row["value"] = key.value
                dict.append(row)

            _json = jsonify(dict)

            if (len(dict) == 0):
                # böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("!!! DBService getChartKV ERROR !!!", err)

    def treeData2(self, params):
             # params = {name:'xx', cid:'xx'} olduğu varsayılıyor
        try:

            # f_chart_tree -> cid, name, data[]
            sql = " select * from f_chart_tree({name!r},{cid}) ".format(
                **params)

            result = self.session.execute(sql)

            dict = {"name": "Kurum"}
            children1 = []

            for key in result:
                row = {"name": key.name}
                children2 = []
                data = key.data
                arr = []
                for i in data:
                    for k in i:
                        arr.append(k)

                # distinct
                arr = list(set(arr))

                for j in arr:
                    children2.append({"name": j, "value": j})
                row["children"] = children2
                children1.append(row)

            dict["children"] = children1
            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("!!! Chart Data Query Failure !!!", err)

    def treeData(self, params):
        try:
            cidName = getCidName(params.get('cid'))
            # f_chart_tree -> cid, name, data[]
            sql = " select * from f_chart_tree({name!r},{cid}) ".format(
                **params)

            result = self.session.execute(sql)

            dict = {"name": cidName}
            children1 = []

            for key in result:
                row = {"name": key.name}
                children2 = []
                data = key.data
                arr = []
                for i in data:
                    arr.append(i)

                # distinct
                arr = list(set(arr))

                for j in arr:
                    children2.append({"name": j, "value": j})
                row["children"] = children2
                children1.append(row)

            dict["children"] = children1
            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("!!! Chart Data Query Failure !!!", err)

    def mapData(self, params):
        try:
            cid = params.get('cid')

            sql = """
                                select name, value, maxvalue from chart_map where cid={0}
                              """.format(cid)

            result = self.session.execute(sql)

            dict = []
            for key in result:
                row = {"name": key.name, "value": key.value,
                       "maxvalue": key.maxvalue}
                dict.append(row)

            # print(dict)

            _json = jsonify(dict)

            if (len(dict) == 0):
                return Response([])
            else:
                return _json

        except Exception as err:
            return Response("!!! Chart World eMAP Data Query Failure !!!", err)


def chartsGateway(params):
    name = params.get('name')
    type = params.get('type')
    cc = Chart()

    # pie ve bar -> cid, name, value döner.. cid-> name :string, value: int değeri dönerken; bar-> name ve value [array] değerleri döner.
    if (type == "pie" and name in ['kv', 'profil', 'birim', 'bolum', 'surec', 'kurumlar_data', 'sistemler_data', 'ortamlar_data', 'ulkeler_data']):
        return cc.kvData(params)
    elif (type == "bar"):
        return cc.barData(params)
    elif (type == "map"):
        return cc.mapData(params)
    elif (type == "tree" and name in ['profil', 'birim', 'bolum', 'surec']):
        return cc.treeData(params)
    # elif (id == "05"):
    #         return cc.chart(ModelChartTalepler,  params)
    else:
        return Response('CHART ID FOR MODEL NOT FOUND!')
