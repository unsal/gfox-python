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

        dict = []
        dict.append(['name', 'manager', 'tooltip'])
        dict.append([cidName, '', 'Kurum Adi'])  # kök organizasyon adı

        bolumId = 0
        for birim in birimler:
            dict.append([birim.birim_name, cidName, 'Birim'])

            for bolum in birim.bolumler_data:
                bolumId += 1
                bolumName = bolum + " ({:0>2d})".format(bolumId)  # aynı bölüm ve birim ismine sahip farklı birimlere bağlanmak için

                dict.append([bolumName, birim.birim_name, 'Bölüm'])

                surecler = session.query(ModelViewBolumSurecler).filter_by(cid=cid, birim_name=birim.birim_name, bolum_name=bolum).limit(1)

                # bir kayıt döndürür varsayarak
                for record in surecler:
                    surecId = 0
                    for surec in record.surecler_data:
                        surecId += 1
                        surecName = surec + " ({:0>2d}".format(bolumId) + "{:0>2d})".format(surecId)  # aynı süreç ismine sahip farklı bölümlere bağlanabilmesi için
                        dict.append([surecName, bolumName, 'Süreç'])

        _json = jsonify(dict)

        if (len(dict) == 0):
            return Response([])
        else:
            return _json

    except Exception as err:
        return Response("!!! Chart Data Query Failure !!!", err)


