from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
import json
from array import array
from db.model import KVTaleplerModel
from api.tanimlar.common import str2bool

class KVTalepler():
        def __init__(self,modelClass):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = modelClass

        def __del__(self):
                self.session.close()

        def get(self):
                try:
                        dict = []

                        sql =  """
                               select base.pidm, base.isim, base.profiller_data, base.tckno, base.dogumtarihi,
                                      base.eposta, base.tel, base.incelemedurumu, i.name islemdurumu,
                                      base.sureuzatma, base.kurumu, base.bilgitalebi, base.timestamp
                               from kv_talepler base, islem_durumlari i
                               where base.islemdurumu = i.pidm
                               order by base.timestamp
                               """

                        data = self.session.execute(sql)

                        for row in data:
                                profillerData = self.createDict('profiller', row.profiller_data ) #create as json[{pidm, name}]

                                dict.append({
                                                'pidm':row.pidm,
                                                'isim':row.isim ,
                                                'profiller_data':profillerData,
                                                'tckno':row.tckno,
                                                'dogumtarihi':row.dogumtarihi,
                                                'eposta':row.eposta,
                                                'tel':row.tel,
                                                'incelemedurumu':row.incelemedurumu,
                                                'islemdurumu':row.islemdurumu,
                                                'sureuzatma':row.sureuzatma,
                                                'kurumu':row.kurumu,
                                                'bilgitalebi':row.bilgitalebi,
                                                'timestamp':row.timestamp
                                        })

                        _json = jsonify(dict)

                        if (len(dict) == 0):
                                return Response([])
                        else:
                                return _json

                except Exception as e:
                        return Response("KVTalepler().get() -> DB SQL Exception! ",e)

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("ADD Successfully")
                        return '', 204

                except Exception as e:
                        return Response("Verbis>KVTalepler>DB Add Exception! ",e)

        # verbis > ekranlarında multiple veriye sahip hücrelere kaynaktan dönen pidmları [{pidm, name}] olarak dönmek için
        def createDict( self, tableName, data ):
        #create dict[pidm, name] from data[pidm]
                try:
                        dict = []
                        items = array('i', data)

                        for item in items:
                                table_pidm = item
                                table_name = self.getPidmName(tableName, table_pidm )
                                dict.append({'pidm':table_pidm, 'name':table_name})

                        if (len(dict) == 0):
                                return []
                        else:
                                return dict

                except Exception:
                        return []

        # for converting json pidm -> names
        def getPidmName(self, tableName, pidm):
                try:
                        sql =  """
                                select  {0}.name
                                from    {0}
                                where   {0}.pidm={1}
                                limit 1
                                """.format(tableName, pidm)

                        data = self.session.execute(sql)
                        name = ""
                        for row in data:
                                name = row.name
                        return name

                except Exception:
                        return "Error!"

def get_kvtalepler():
    model = KVTaleplerModel()
    cc = KVTalepler(model)
    return cc.get()


def add_kvtalepler(data):

        print(data)

        isim_ = data.get('isim')
        profiller_data_ = data.get('profiller_data')
        tckno_ = data.get('tckno')
        dogumtarihi_ = data.get('dogumtarihi')
        eposta_ = data.get('eposta')
        tel_ = data.get('tel')
        incelemedurumu_ = data.get('incelemedurumu')
        islemdurumu_ = data.get('islemdurumu')
        sureuzatma_ = data.get('sureuzatma')
        kurumu_ = data.get('kurumu')
        bilgitalebi_ = data.get('bilgitalebi')

        # return ""
        model = KVTaleplerModel(
                                isim=isim_,
                                profiller_data = profiller_data_,
                                tckno=tckno_,
                                dogumtarihi = dogumtarihi_,
                                eposta=eposta_,
                                tel=tel_,
                                incelemedurumu=incelemedurumu_,
                                islemdurumu=islemdurumu_,
                                sureuzatma=sureuzatma_,
                                kurumu=kurumu_,
                                bilgitalebi=bilgitalebi_
                                )
        cc=KVTalepler(model)
        return cc.add()





