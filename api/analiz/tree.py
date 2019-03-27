from flask import Response
from flask import jsonify
from db.model import *
from api.gfox import *


def treeData(session, params):
    try:
        cidName = getCidName(params.get('cid'))
        # f_chart_tree -> cid, name, data[]
        sql = " select * from f_chart_tree({name!r},{cid}) ".format(
            **params)

        result = session.execute(sql)

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
