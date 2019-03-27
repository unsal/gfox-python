from flask import Response
from flask import jsonify


def mapData(session, params):
    try:
        cid = params.get('cid')

        sql = """
                            select name, value, maxvalue from chart_map where cid={0}
                            """.format(cid)

        result = session.execute(sql)

        dict = []
        for key in result:
            row = {"name": key.name, "value": key.value, "maxvalue": key.maxvalue}
            dict.append(row)

        # print(dict)

        _json = jsonify(dict)

        if (len(dict) == 0):
            return Response([])
        else:
            return _json

    except Exception as err:
        return Response("!!! Chart World eMAP Data Query Failure !!!", err)
