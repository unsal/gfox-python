# Veritabanı bağlantısı için
class ConfigLocal:
        # HOST = "bt.ozyegin.edu.tr:5432"
        HOST = "localhost:5432"
        DATABASE = "gfox"
        USER = "postgres"
        PASSWORD = "Qaz1wsx2!"

class ConfigOZU:
        # HOST = "bt.ozyegin.edu.tr:5432"
        HOST = "bt.ozyegin.edu.tr:5432"
        DATABASE = "gfox"
        USER = "gfox"
        PASSWORD = "Qaz1wsx2!"

# class ConfigAWS:
#         HOST = "mydbinstance.cnyxtuppiqxw.eu-west-1.rds.amazonaws.com"
#         DATABASE = "gfox"
#         USER = "gfox"
#         PASSWORD = "Qaz1wsx2!"

# class ConfigGCP:
#         HOST = "35.205.60.74"
#         DATABASE = "gfox"
#         USER = "gfox"
#         PASSWORD = "Qaz1wsx2!"

class ConfigJWT:
        SECRETKEY = 'f8ab9dbb04441f985ff81985ea14a0c0'
