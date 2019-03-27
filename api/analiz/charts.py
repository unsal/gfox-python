# - *- coding: utf- 8 - *-
from flask import Response
from db.connection import Connect
from api.analiz.pie import pieData
from api.analiz.bar import barData
from api.analiz.tree import treeData
from api.analiz.geo import geoData
from api.analiz.org import orgData


def getChartData(params):

    conn = Connect()
    session = conn.session()

    name = params.get('name')
    type = params.get('type')

    # pie ve bar -> cid, name, value döner.. cid-> name :string, value: int değeri dönerken; bar-> name ve value [array] değerleri döner.
    if (type == "pie" and name in ['kv', 'profil', 'birim', 'bolum', 'surec', 'kurumlar_data', 'sistemler_data', 'ortamlar_data', 'ulkeler_data']):
        return pieData(session, params)
    elif (type == "bar"):
        return barData(session, params)
    elif (type == "geo"):
        return geoData(session, params)
    elif (type == "tree" and name in ['profil', 'birim', 'bolum', 'surec']):
        return treeData(session, params)
    elif (type == "org"):
        return orgData(session, params)
    else:
        return Response('CHART ID FOR MODEL NOT FOUND!')

    session.close()
