from db.connection import Connect
from flask import Response


class Gfox ():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    # GET query results

    def getCidName(self, cid):
        try:
            sql = "select name from t_cid where pidm={0} limit 1".format(
                cid)
            result = self.session.execute(sql)

            name = ""
            for item in result:
                name = item.name

            return name

        except Exception:
            return "Error!"

    def isAdminUser(self, uid):
        try:
            filter = {"uid": uid}
            sql = "select 1 from auth_login where uid={uid!r} and admin=true limit 1".format(**filter)
            result = self.session.execute(sql)

            admin = False
            for exist in result:
                admin = True

            print("admin? ", admin)

            return admin

        except Exception as err:
            print("Exception Error: ", err)
            return Response("!!! PieChart API Error !!!", err)


def getCidName(cid):
    cc = Gfox()
    return cc.getCidName(cid)


def isAdminUser(uid):
    cc = Gfox()
    return cc.isAdminUser(uid)

