from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean, JSON)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

#_Base tek _ underscore private olduğu ve  dışardan import edilemeyeceği anlamnıa geliyor.
# tek _ classlar için, __ çifti tanım ve fonksiyonlar için
_Base = declarative_base()

# TANIMLAR ********************************************************
# Custom base class
class TanimlarBase(object):
    pidm = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.now())

class Profiller(TanimlarBase, _Base):
    __tablename__ = 'profiller'

class Birimler(TanimlarBase, _Base):
    __tablename__ = 'birimler'

class KV(TanimlarBase, _Base):
    __tablename__ = 'kv'

class IslemeAmaclari(TanimlarBase, _Base):
    __tablename__ = 'isleme_amaclari'

class Kanallar(TanimlarBase, _Base):
    __tablename__ = 'kanallar'

class Sistemler(TanimlarBase, _Base):
    __tablename__ = 'sistemler'
    local = Column(Boolean())

class Dokumanlar(TanimlarBase, _Base):
    __tablename__ = 'dokumanlar'

class Dayanaklar(TanimlarBase, _Base):
    __tablename__ = 'dayanaklar'

class Ortamlar(TanimlarBase, _Base):
    __tablename__ = 'ortamlar'

class Sureler(TanimlarBase, _Base):
    __tablename__ = 'sureler'

class Kurumlar(TanimlarBase, _Base):
    __tablename__ = 'kurumlar'

class PaylasimAmaclari(TanimlarBase, _Base):
    __tablename__ = 'paylasim_amaclari'

class PaylasimSekilleri(TanimlarBase, _Base):
    __tablename__ = 'paylasim_sekilleri'

class Ulkeler(TanimlarBase, _Base):
    __tablename__ = 'ulkeler'
    phone_area = Column(String(3))
    secure = Column(Boolean())

#pidm ve name olduğu için tanim bölümündeki standart modelden yararlandım
class YayinDurumlari(TanimlarBase, _Base):
    __tablename__ = 'ss_yayindurumu'

#KV TALEPLER Tablosu için
class IslemDurumlari(TanimlarBase, _Base):
    __tablename__ = 'islem_durumlari'


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
      KVSistemler = "sistemler"
      SaklamaSuresi = "sureler"
      GuvenliUlkeler = "ulkeler"
      YayinDurumlari = "yayindurumlari"
      IslemDurumlari = "islemdurumlari"

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
    elif (id==TanimlarID.YayinDurumlari):
            model = YayinDurumlari
    elif (id==TanimlarID.IslemDurumlari):
            model = IslemDurumlari
    else:
            model = None

    return model



# SS *********************************
class SSCommonBase(object):
    pidm = Column(Integer(), primary_key=True)
    birim_pidm = Column(Integer())
    timestamp = Column(TIMESTAMP, default=datetime.now())

class SSKurumlarModel(SSCommonBase, _Base):
    __tablename__ = 'ss_kurumlar'
    kurum_pidm = Column(Integer())

class SSKanallarModel(SSCommonBase, _Base):
    __tablename__ = 'ss_toplama_kanallari'
    kanal_pidm = Column(Integer())

class SSSistemlerModel(SSCommonBase, _Base):
    __tablename__ = 'ss_kullanilan_sistemler'
    sistem_pidm = Column(Integer())

class SSDokumanlarModel(_Base):
    __tablename__ = 'ss_dokumanlar'
    pidm = Column(Integer(), primary_key=True)
    birim_pidm = Column(Integer())
    dokuman_pidm = Column(Integer())
    yayin_pidm = Column(Integer())
    timestamp = Column(TIMESTAMP, default=datetime.now())



# VERBIS MODEL

class KVBaseModel(object):
    # otomatik oluşturulan alanlar
    pidm = Column(Integer(), primary_key=True)
    timestamp = Column(TIMESTAMP, default=datetime.now())


class KVProfilModel(KVBaseModel, _Base):
    __tablename__ = 'kv_profil'
    # yazilimdan geleceklre
    profil_pidm = Column(Integer())
    birim_pidm = Column(Integer())
    data = Column(JSON()) #format:[{"kv_pidm":"179"},{"kv_pidm":"181"}]


class KVPaylasimModel(KVBaseModel, _Base):
    __tablename__='kv_paylasim'
    #paylasim
    birim_pidm = Column(Integer())
    kv_pidm = Column(Integer())
    kurum_pidm = Column(Integer())
    islemeamaclari_data = Column(JSON())
    paylasimamaclari_data = Column(JSON())
    paylasimsekilleri_data = Column(JSON())


class KVAnaveriModel(KVBaseModel, _Base):
    __tablename__='kv_anaveri'
    birim_pidm= Column(Integer())
    kv_pidm = Column(Integer())
    #anaveri
    sure_pidm =Column(Integer)
    ulkeler_data = Column(JSON())
    kanallar_data = Column(JSON())
    dokumanlar_data = Column(JSON()) #kanal_pidms
    sistemler_data= Column(JSON()) #dokuman_pidms
    dayanaklar_data = Column(JSON()) #sistem_pidms
    ortamlar_data = Column(JSON())

# *******************  KV TALEPLERI  ********************
class KVTaleplerModel(KVBaseModel, _Base):
    __tablename__='kv_talepleri'
    pidm= Column(Integer(), primary_key=True)

    isim = Column(String(60))
    profiller_data = Column(JSON())
    tckno = Column(String(11))
    dogumtarihi = Column(String(10))
    eposta = Column(String(30))
    tel = Column(String(15))
    incelemedurumu = Column(String(255))
    islemdurumu = Column(Integer())
    sureuzatma = Column(Boolean(), default=False)
    kurumu = Column(String(60))
    bilgitalebi = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.now())











