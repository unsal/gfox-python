from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

#_Base tek _ underscore private olduğu ve  dışardan import edilemeyeceği anlamnıa geliyor.
# tek _ classlar için, __ çifti tanım ve fonksiyonlar için
_Base = declarative_base()

# TANIMLAR ********************************************************
# Custom base class
class Tanimlar(object):
    pidm = Column(Integer(), primary_key=True, autoincrement=True)
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
    local = Column(Boolean())

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

# SS *********************************
class SSKurumlarModel(_Base):
    __tablename__ = 'ss_kurumlar'
    pidm = Column(Integer(), primary_key=True)
    birim_pidm = Column(Integer())
    kurum_pidm = Column(Integer())
    timestamp = Column(TIMESTAMP, default=datetime.now())

class SSDokumanlarModel(_Base):
    __tablename__ = 'ss_dokumanlar'
    pidm = Column(Integer(), primary_key=True)
    birim_pidm = Column(Integer())
    dokuman_pidm = Column(Integer())
    yayin_pidm = Column(Integer())
    timestamp = Column(TIMESTAMP, default=datetime.now())

# react tarafından post edilen ID'leri tek noktadan kolayca yönetebilmek için yazıldı.
class TanimlarID():
      Profiller = "profiller"
      Birimler = "birimler"
      Dayanaklar = "dayanaklar"
      Dokumanlar = "dokumanlar"
      IslemeAmaclari = "islemeamaclari"
      ToplamaKanallari = "kanallar"
      Kurumlar = "kurumlar"
      KV = "kv"
      ArsivOrtamlari = "ortamlar"
      PaylasimAmaclari = "paylasimamaclari"
      PaylasimSekilleri = "paylasimsekilleri"
      KVSistemler = "kvsistemler"
      SaklamaSuresi = "sureler"
      GuvenliUlkeler = "ulkeler"

def getModel(id):
    if (id == TanimlarID.Profiller):
            model = Profiller
    elif (id==TanimlarID.Birimler):
            model = Birimler
    elif (id==TanimlarID.Dayanaklar):
            model = Dayanaklar
    elif (id==TanimlarID.Dokumanlar):
            model = Dokumanlar
    elif (id==TanimlarID.IslemeAmaclari):
            model = IslemeAmaclari
    elif (id==TanimlarID.ToplamaKanallari):
            model = Kanallar
    elif (id==TanimlarID.KV):
            model = KV
    elif (id==TanimlarID.ArsivOrtamlari):
            model = Ortamlar
    elif (id==TanimlarID.KVSistemler):
            model=Sistemler
    elif (id==TanimlarID.SaklamaSuresi):
            model = Sureler
    elif (id==TanimlarID.Kurumlar):
            model = Kurumlar
    elif (id==TanimlarID.PaylasimAmaclari):
            model = PaylasimAmaclari
    elif (id==TanimlarID.PaylasimSekilleri):
            model = PaylasimSekilleri
    elif (id==TanimlarID.GuvenliUlkeler):
            model = Ulkeler
    else:
            model = None

    return model







