from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
import json
from array import array

class KVBase():
        def __init__(self,model):
                self.conn = Connect()
                self.session = self.conn.session()
                self.model = model

        def __del__(self):
                self.session.close()

        def add(self):
                try:
                        self.session.add(self.model)
                        self.session.commit()
                        print("ADD Successfully")
                        return '', 204

                except Exception as e:
                        return Response("Verbis>KVPaylasim>DB Add Exception! ",e)

        def update(self):
                try:
                        pidm_ = int(self.model.pidm)
                        newData = self.model.data
                        row = self.session.query( self.model.__class__).filter_by(pidm=pidm_).one()
                        row.data =newData
                        self.session.commit()
                        print("Update Successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on update ", err)
                        return '', 404

        #Delete entire row
        def delete(self):
                try:
                        pidm_ = int(self.model.pidm)
                        row = self.session.query(
                        self.model.__class__).filter_by(pidm=pidm_).one()
                        self.session.delete(row)
                        self.session.commit()
                        print("deleted successfully")
                        return '', 204
                except Exception as err:
                        print("DB Error on deleting ", err)
                        return '', 404

        # for converting json pidm -> names
        def getPidmName(self, tableName, pidm, cid):
                try:
                        sql =  """
                                select  {0}.name
                                from    {0}
                                where   {0}.pidm={1} and {0}.cid={2}
                                limit 1
                                """.format(tableName, pidm, cid)

                        data = self.session.execute(sql)
                        name = ""
                        for row in data:
                                name = row.name
                        return name

                except Exception:
                        return "Error!"

        # verbis > ekranlarında multiple veriye sahip hücrelere kaynaktan dönen pidmları [{pidm, name}] olarak dönmek için
        def createDict( self, tableName, data, cid ):
        #create dict[pidm, name] from data[pidm]
                try:
                        dict = []
                        items = array('i', data)

                        for item in items:
                                table_pidm = item
                                table_name = self.getPidmName(tableName, table_pidm ,cid)
                                dict.append({'pidm':table_pidm, 'name':table_name})

                        if (len(dict) == 0):
                                return []
                        else:
                                return dict

                except Exception:
                        return []

