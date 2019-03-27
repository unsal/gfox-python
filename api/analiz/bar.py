from flask import Response
from flask import jsonify


def barData(session, params):
    try:
        # params = {name:'xx', cid:'xx'} olduğu varsayılıyor
        # {name!r} => sonucu tırnaklı string olarak basmak için => " 'xx' "
        sql = " select * from f_chart_kv_bar({name!r},{cid}) ".format(
            **params)

        result = session.execute(sql)

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
