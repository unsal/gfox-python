from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean, JSON)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify
from flask import Response

#_Base tek _ underscore private olduğu ve  dışardan import edilemeyeceği anlamnıa geliyor.
# tek _ classlar için, __ çifti tanım ve fonksiyonlar için
_Base = declarative_base()

# TANIMLAR ********************************************************
# Custom base class
class TanimlarBase(object):
    pidm = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))

class Profiller(TanimlarBase, _Base):
    __tablename__ = 'profiller'

class Birimler(TanimlarBase, _Base):
    __tablename__ = 'birimler'

class KV(TanimlarBase, _Base):
    __tablename__ = 'kv'
    kv_kategoriler_pidm = Column(Integer())

class KVKategoriler(TanimlarBase, _Base):
    __tablename__ = 'kv_kategoriler'

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

class Tedbirler(TanimlarBase, _Base):
    __tablename__ = 'tedbirler'


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
      KVKategoriler = "kvkategoriler"
      ArsivOrtamlari = "ortamlar"
      PaylasimAmaclari = "paylasimamaclari"
      PaylasimSekilleri = "paylasimsekilleri"
      KVSistemler = "sistemler"
      SaklamaSuresi = "sureler"
      GuvenliUlkeler = "ulkeler"
      YayinDurumlari = "yayindurumlari"
      IslemDurumlari = "islemdurumlari"
      Tedbirler = "tedbirler"

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
    elif (id==TanimlarID.KVKategoriler):
            model = KVKategoriler
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
    elif (id==TanimlarID.Tedbirler):
            model = Tedbirler
    else:
            model = None

    return model



# SS *********************************
class SSCommonBase(object):
    pidm = Column(Integer(), primary_key=True)
    birim_pidm = Column(Integer())
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))

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
    cid = Column(Integer())
    uid = Column(String(60))



# VERBIS MODEL

class KVBaseModel(object):
    # otomatik oluşturulan alanlar
    pidm = Column(Integer(), primary_key=True)
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))


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
    tedbirler_data = Column(JSON())

# *******************  KV TALEPLERI  ********************
class KVTaleplerModel(KVBaseModel, _Base):
    __tablename__='kv_talepleri'
    pidm= Column(Integer(), primary_key=True)
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))

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

class AuthModel(_Base):
    __tablename__='view_auth'
    pidm        = Column('pidm',Integer(), primary_key=True) #SQLAlchemt her tabloda primary_key istediği için eklendi
    uid         = Column('uid',String(60))
    cid         = Column('cid',Integer())
    cid_name    = Column('cid_name',String(60))

class AuthLoginModel(_Base):
    __tablename__='auth_login'
    uid         = Column('uid',String(60), primary_key=True)
    pwd         = Column('pwd', String(255))
    admin       = Column('admin',Boolean(), default=False)
    timestamp = Column(TIMESTAMP, default=datetime.now())


# VIEW MODELS PART
class ViewKVProfilModel(_Base):
    __tablename__ = 'view_kvprofil'
    # yazilimdan geleceklre
    pidm        = Column('pidm',Integer(), primary_key=True)
    cid         = Column('cid',Integer())
    profil_name = Column(String(255))
    birim_name  = Column(String(255))
    data = Column(JSON())
    timestamp = Column(TIMESTAMP)

class ViewKVPaylasimModel(_Base):
    __tablename__ = 'view_kvpaylasim'
    # yazilimdan geleceklre
    pidm        = Column('pidm',Integer(), primary_key=True)
    cid         = Column('cid',Integer())
    birim_name = Column(String(255))
    kv_name  = Column(String(255))
    kurum_name  = Column(String(255))
    islemeamaclari_data = Column(JSON())
    paylasimamaclari_data = Column(JSON())
    paylasimsekilleri_data = Column(JSON())
    timestamp = Column(TIMESTAMP)

class ViewKVAnaveriModel(_Base):
    __tablename__ = 'view_kvanaveri'
    # yazilimdan geleceklre
    pidm        = Column('pidm',Integer(), primary_key=True)
    cid         = Column('cid',Integer())
    birim_name = Column(String(255))
    kv_name  = Column(String(255))
    sure_name  = Column(String(255))
    ulkeler_data = Column(JSON())
    kanallar_data = Column(JSON())
    dokumanlar_data = Column(JSON())
    sistemler_data = Column(JSON())
    dayanaklar_data = Column(JSON())
    ortamlar_data = Column(JSON())
    tedbirler_data = Column(JSON())
    timestamp = Column(TIMESTAMP)


# BOLUMLER -----------------------------------------------
class ModelBolumler(_Base):
    __tablename__ = 'bolumler'
    pidm = Column(Integer(), primary_key=True)
    name = Column(String(255))
    birim_pidm = Column(Integer())
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))

class ModelViewBolumler(_Base):
    __tablename__ = 'view_bolumler'
    birim_pidm = Column(Integer(), primary_key=True)
    birim_name = Column(String(255))
    bolumler_data = Column(JSON())
    cid = Column(Integer())
    uid = Column(String(60))

# SURECLER -----------------------------------------------
class ModelSurecler(_Base):
    __tablename__ = 'surecler'
    pidm = Column(Integer(), primary_key=True)
    name = Column(String(255))
    bolum_pidm = Column(Integer())
    cid = Column(Integer())
    uid = Column(String(60))

class ModelViewSurecler(_Base):
    __tablename__ = 'view_surecler'
    birim_name = Column(String(255))
    bolum_name = Column(String(255))
    bolum_pidm = Column(Integer(), primary_key=True)
    surecler_data = Column(JSON())
    cid = Column(Integer())
    uid = Column(String(60))

#KV -------------------------------------------
class ModelViewKV(_Base):
    __tablename__ = 'view_kv'
    pidm = Column(Integer(), primary_key=True)
    name = Column(String(255))
    kategori_name = Column(String(255))
    cid = Column(Integer())
    uid = Column(String(60))

#KV -------------------------------------------
class ModelAnaveriler(_Base):
    __tablename__ = 'anaveriler'
    pidm = Column(Integer(), primary_key=True)
    profil_pidm = Column(Integer())
    surec_pidm = Column(Integer())
    kv_pidm = Column(Integer())
    sure_pidm = Column(Integer())
    kanal_pidm = Column(Integer())
    sistem_pidm = Column(Integer())
    dayanak_pidm = Column(Integer())
    isleme_amaclari_pidm = Column(Integer())
    ortamlar_data = Column(JSON())
    tedbirler_data = Column(JSON())
    cid = Column(Integer())
    uid = Column(String(60))

class ModelViewAnaveriler(_Base):
    __tablename__ = 'view_anaveriler'
    pidm = Column(Integer(), primary_key=True)
    profil_name = Column(String(255))
    surec_name = Column(String(255))
    kv_name = Column(String(255))
    sure_name = Column(String(255))
    kanal_name = Column(String(255))
    sistem_name = Column(String(255))
    dayanak_name = Column(String(255))
    isleme_amaclari_name = Column(String(255))
    ortamlar_data = Column(JSON())
    tedbirler_data = Column(JSON())
    cid = Column(Integer())
    uid = Column(String(60))






