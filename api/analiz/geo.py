from flask import Response
from flask import jsonify


def geoData(session, params):
    try:
        cid = params.get('cid')

        sql = """
                            select name, value, maxvalue from chart_map where cid={0}
                            """.format(cid)

        result = session.execute(sql)

        dict = [['Ulke', 'Kv']]
        for key in result:
            dict.append([key.name, key.value])

        # print(dict)

        _json = jsonify(dict)

        if (len(dict) == 0):
            return Response([])
        else:
            return _json

    except Exception as err:
        return Response("!!! Chart World eMAP Data Query Failure !!!", err)
