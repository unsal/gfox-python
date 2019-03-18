from db.connection import Connect


class Gfox ():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()

    def __del__(self):
        self.session.close()

    # GET query results

    def getCidName(self, cid):
        try:
            sql = "select name from auth_cid where pidm={0} limit 1".format(
                cid)
            result = self.session.execute(sql)

            name = ""
            for item in result:
                name = item.name

            return name

        except Exception:
            return "Error!"


def getCidName(cid):
    cc = Gfox()
    return cc.getCidName(cid)
