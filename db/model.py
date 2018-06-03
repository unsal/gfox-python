from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

#_Base tek _ underscore private olduğu ve  dışardan import edilemeyeceği anlamnıa geliyor.
# tek _ classlar için, __ çifti tanım ve fonksiyonlar için
_Base = declarative_base()

# Custom base class
class Tanimlar(object):
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.now())

class Profiller(Tanimlar, _Base):
    __tablename__ = 'profiller'

class Birimler(Tanimlar, _Base):
    __tablename__ = 'birimler'

class KV(Tanimlar, _Base):
    __tablename__ = 'kv'

class IslemeAmaclari(Tanimlar, _Base):
    __tablename__ = 'isleme_amaclari'

class Kanallar(Tanimlar, _Base):
    __tablename__ = 'kanallar'

class Sistemler(Tanimlar, _Base):
    __tablename__ = 'sistemler'
    type = Column(String(30))

class Dokumanlar(Tanimlar, _Base):
    __tablename__ = 'dokumanlar'

class Dayanaklar(Tanimlar, _Base):
    __tablename__ = 'dayanaklar'

class Ortamlar(Tanimlar, _Base):
    __tablename__ = 'ortamlar'

class Sureler(Tanimlar, _Base):
    __tablename__ = 'sureler'

class Kurumlar(Tanimlar, _Base):
    __tablename__ = 'kurumlar'

class PaylasimAmaclari(Tanimlar, _Base):
    __tablename__ = 'paylasim_amaclari'

class PaylasimSekilleri(Tanimlar, _Base):
    __tablename__ = 'paylasim_sekilleri'

class Ulkeler(Tanimlar, _Base):
    __tablename__ = 'ulkeler'
    phone_area = Column(String(3))
    secure = Column(Boolean())





