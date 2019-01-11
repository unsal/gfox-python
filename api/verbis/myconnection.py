from flask import Response
from flask import jsonify
from flask import abort
from flask import request
from db.connection import Connect
import json
from array import array

class MyConnection():
        def __init__(self):
                self.conn = Connect()
                self.session = self.conn.session()

        def __del__(self):
                self.session.close()

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
                        items = array('i', data) #array as integer 'i'

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

