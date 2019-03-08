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

        def kvData(self, params):
                try:
                        # params = {name:'xx', cid:'xx'} olduğu varsayılıyor
                        # {name!r} => sonucu tırnaklı string olarak basmak için => " 'xx' "
                        sql = " select * from f_chart_kv({name!r},{cid}) limit 10 ".format(**params)

                        result = self.session.execute(sql)

                        dict = []
                        for key in result:
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
                        return Response("!!! DBService getChartKV ERROR !!!", err)

        # def chart(self, model, params):
        #         try:
        #                 cid_ = params.get('cid')

        #                 data = self.session.query(model).filter_by(cid=cid_).limit(10).all()

        #                 dict = []
        #                 for key in data:
        #                         row = {}
        #                         row["name"]=key.name
        #                         row["value"]=key.value
        #                         dict.append(row)

        #                 _json = jsonify(dict)


        #                 if (len(dict) == 0):
        #                         return Response([]) #böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
        #                 else:
        #                         return _json

        #         except Exception as err:
        #                 return Response("!!! Chart Data Query Failure !!!", err)

        def treeArray (self, model, params):
                try:
                        cid_ = params.get('cid')
                        result = self.session.query(model).filter_by(cid=cid_)

                        dict = {"name":"Kurum"}
                        children1 = []

                        for key in result:
                                row = {"name":key.name}
                                children2 = []
                                data = key.data
                                arr = []
                                for i in data:
                                        for k in i:
                                                arr.append(k)

                                #distinct
                                arr = list(set(arr))

                                for j in arr:
                                        children2.append({"name":j,"value":j})
                                row["children"] = children2
                                children1.append(row)

                        dict["children"] = children1
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except  Exception as err:
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
                                arr = []
                                for i in data:
                                     arr.append(i)

                                #distinct
                                arr = list(set(arr))

                                for j in arr:
                                        children2.append({"name":j,"value":j})
                                row["children"] = children2
                                children1.append(row)

                        dict["children"] = children1
                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except  Exception as err:
                        return Response("!!! Chart Data Query Failure !!!", err)


        def mapData (self,params):
                try:
                        cid = params.get('cid')

                        sql = """
                                select name, value, maxvalue from chart_map where cid={0}
                              """.format(cid)

                        result = self.session.execute(sql)

                        dict = []
                        for key in result:
                                row = {"name":key.name, "value":key.value, "maxvalue":key.maxvalue}
                                dict.append(row)

                        # print(dict)

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json


                except  Exception as err:
                        return Response("!!! Chart World eMAP Data Query Failure !!!", err)


def chartsGateway(params):
        name = params.get('name')
        cc = Chart()

        if (name in ['kv','profil','birim','bolum','surec','kurumlar_data','sistemler_data','ulkeler_data']):
                return cc.kvData(params)
        elif (name == "map"):
                return cc.mapData(params)
        # elif (id == "02"):
        #         return cc.chart(ModelCharKVKurum,  params)
        # elif (id == "03"):
        # elif (id == "05"):
        #         return cc.chart(ModelChartTalepler,  params)
        # elif (id == "06"):
        #         return cc.treeKV(ModelChartTreeBirimKV,params)
        # elif (id == "07"):
        #         return cc.treeKV(ModelChartTreeProfilKV,params)
        # elif (id == "08"):
        #         return cc.treeArray(ModelChartTreeBirimKurum,params)
        else:
                return Response('CHART ID FOR MODEL NOT FOUND!')

