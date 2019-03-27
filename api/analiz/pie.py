# - *- coding: utf- 8 - *-
from flask import Response
from flask import jsonify


def pieData(session, params):
    try:
        # params = {name:'xx', cid:'xx'} olduğu varsayılıyor
        # {name!r} => sonucu tırnaklı string olarak basmak için => " 'xx' "
        sql = " select * from f_chart_kv({name!r},{cid}) order by value desc limit 20".format(
            **params)

        result = session.execute(sql)

        dict = [['name', 'value']]
        for key in result:
            dict.append([key.name, key.value])

        _json = jsonify(dict)

        if (len(dict) == 0):
            # böyle  [] yapmazsan react tarafında data.map funciton not found hatası alırsın!!
            return Response([])
        else:
            return _json

    except Exception as err:
        return Response("!!! PieChart API Error !!!", err)
