# - *- coding: utf- 8 - *-
from flask import Response
from flask import jsonify
from db.model import ModelViewBirimBolumler, ModelViewBolumSurecler
from api.gfox import getCidName


def orgData(session, params):
    # Output: {name: xxx, children: [{name: 'aaaa', children: {name: 'iiii', value: 1}], ..}]}
    try:
        cid = params.get('cid')
        cidName = getCidName(cid)
        birimler = session.query(ModelViewBirimBolumler).filter_by(cid=cid)

        dict = {"name": cidName}
        childrenBirim = []

        for birim in birimler:
            birimName = birim.birim_name
            bolumlerArray = birim.bolumler_data

            childrenBolum = []
            for bolum in bolumlerArray:
                surecler = session.query(ModelViewBolumSurecler).filter_by(cid=cid, birim_name=birimName, bolum_name=bolum).limit(1)

                for record in surecler:
                    sureclerArray = record.surecler_data

                    sureclerJson = []
                    for surec in sureclerArray:
                        sureclerJson.append({"name": surec, "value": 1})

                childrenBolum.append({"name": bolum, "children": sureclerJson})

            childrenBirim.append({"name": birimName, "children": childrenBolum})

        dict["children"] = childrenBirim
        _json = jsonify(dict)

        if (len(dict) == 0):
            return Response([])
        else:
            return _json

    except Exception as err:
        return Response("!!! Chart Data Query Failure !!!", err)


