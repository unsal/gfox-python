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

class FrameworkBase(object):
    pidm = Column(Integer(), primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))

class TanimlarBase(object):
    pidm = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(60))


# TANIMLAR -------------------------------------------
class ModelProfiller(TanimlarBase, _Base):
    __tablename__ = 'profiller'

class ModelDayanaklar(TanimlarBase, _Base):
    __tablename__ = 'dayanaklar'

class ModelBirimler(TanimlarBase, _Base):
    __tablename__ = 'birimler'

class ModelKV(TanimlarBase, _Base):
    __tablename__ = 'kv'
    kv_kategoriler_pidm = Column(Integer())

class ModelKVKategoriler(TanimlarBase, _Base):
    __tablename__ = 'kv_kategoriler'

class ModelIslemeAmaclari(TanimlarBase, _Base):
    __tablename__ = 'isleme_amaclari'

class ModelKanallar(TanimlarBase, _Base):
    __tablename__ = 'kanallar'

class ModelSistemler(TanimlarBase, _Base):
    __tablename__ = 'sistemler'
    local = Column(Boolean())

class ModelDokumanlar(TanimlarBase, _Base):
    __tablename__ = 'dokumanlar'

class ModelOrtamlar(TanimlarBase, _Base):
    __tablename__ = 'ortamlar'

class ModelSureler(TanimlarBase, _Base):
    __tablename__ = 'sureler'

class ModelKurumlar(TanimlarBase, _Base):
    __tablename__ = 'kurumlar'

class ModelPaylasimAmaclari(TanimlarBase, _Base):
    __tablename__ = 'paylasim_amaclari'

class ModelPaylasimSekilleri(TanimlarBase, _Base):
    __tablename__ = 'paylasim_sekilleri'

class ModelUlkeler(TanimlarBase, _Base):
    __tablename__ = 'ulkeler'
    phone_area = Column(String(3))
    secure = Column(Boolean())

#pidm ve name olduğu için tanim bölümündeki standart modelden yararlandım
class ModelYayinDurumlari(TanimlarBase, _Base):
    __tablename__ = 'ss_yayindurumu'

#KV TALEPLER Tablosu için
class ModelIslemler(TanimlarBase, _Base):
    __tablename__ = 'islemler'

class ModelTedbirler(TanimlarBase, _Base):
    __tablename__ = 'tedbirler'


# react tarafından post edilen ID'leri tek noktadan kolayca yönetebilmek için yazıldı.
class ModelID():
      Profiller = "profiller"
      Birimler = "birimler"
      Dayanaklar = "dayanaklar"
      Sureler = "sureler"
      IslemeAmaclari = "islemeamaclari"
      ToplamaKanallari = "kanallar"
      Kurumlar = "kurumlar"
      KV = "kv"
      KVKategoriler = "kvkategoriler"
      ArsivOrtamlari = "ortamlar"
      PaylasimAmaclari = "paylasimamaclari"
      PaylasimSekilleri = "paylasimsekilleri"
      KVSistemler = "sistemler"
      GuvenliUlkeler = "ulkeler"
      YayinDurumlari = "yayindurumlari"
      Islemler = "islemler"
      Tedbirler = "tedbirler"
      Surecler = "surecler"

def getModel(id):
    if (id == ModelID.Profiller):
            model = ModelProfiller
    elif (id==ModelID.Birimler):
            model = ModelBirimler
    elif (id==ModelID.Dayanaklar):
            model = ModelDayanaklar
    elif (id==ModelID.IslemeAmaclari):
            model = ModelIslemeAmaclari
    elif (id==ModelID.ToplamaKanallari):
            model = ModelKanallar
    elif (id==ModelID.KV):
            model = ModelKV
    elif (id==ModelID.KVKategoriler):
            model = ModelKVKategoriler
    elif (id==ModelID.ArsivOrtamlari):
            model = ModelOrtamlar
    elif (id==ModelID.KVSistemler):
            model=ModelSistemler
    elif (id==ModelID.Sureler):
            model = ModelSureler
    elif (id==ModelID.Kurumlar):
            model = ModelKurumlar
    elif (id==ModelID.PaylasimAmaclari):
            model = ModelPaylasimAmaclari
    elif (id==ModelID.PaylasimSekilleri):
            model = ModelPaylasimSekilleri
    elif (id==ModelID.GuvenliUlkeler):
            model = ModelUlkeler
    elif (id==ModelID.YayinDurumlari):
            model = ModelYayinDurumlari
    elif (id==ModelID.Islemler):
            model = ModelIslemler
    elif (id==ModelID.Tedbirler):
            model = ModelTedbirler
    else:
            model = None

    return model

#özel optionslar için...
def getOptionsModel(id):
    if (id == ModelID.Surecler):
            model = ModelOptionsSurecler
    elif (id == ModelID.Profiller):
            model = ModelProfiller
    elif (id==ModelID.Birimler):
            model = ModelBirimler
    elif (id==ModelID.Dayanaklar):
            model = ModelDayanaklar
    elif (id==ModelID.IslemeAmaclari):
            model = ModelIslemeAmaclari
    elif (id==ModelID.ToplamaKanallari):
            model = ModelKanallar
    elif (id==ModelID.KV):
            model = ModelKV
    elif (id==ModelID.KVKategoriler):
            model = ModelKVKategoriler
    elif (id==ModelID.ArsivOrtamlari):
            model = ModelOrtamlar
    elif (id==ModelID.KVSistemler):
            model=ModelSistemler
    elif (id==ModelID.Sureler):
            model = ModelSureler
    elif (id==ModelID.Kurumlar):
            model = ModelKurumlar
    elif (id==ModelID.PaylasimAmaclari):
            model = ModelPaylasimAmaclari
    elif (id==ModelID.PaylasimSekilleri):
            model = ModelPaylasimSekilleri
    elif (id==ModelID.GuvenliUlkeler):
            model = ModelUlkeler
    elif (id==ModelID.YayinDurumlari):
            model = ModelYayinDurumlari
    elif (id==ModelID.Islemler):
            model = ModelIslemler
    elif (id==ModelID.Tedbirler):
            model = ModelTedbirler
    else:
        #diğer optionsları getModelden alıyor.. burası özel options için
            model = None

    return model


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

#KV -------------------------------------------
class ModelViewKV(_Base):
    __tablename__ = 'view_kv'
    pidm = Column(Integer(), primary_key=True)
    name = Column(String(255))
    kategori_name = Column(String(255))
    cid = Column(Integer())
    uid = Column(String(60))

#KV -------------------------------------------
class ModelAnaveriler(FrameworkBase, _Base):
    __tablename__ = 'anaveriler'
    profil_pidm = Column(Integer())
    surec_pidm = Column(Integer())
    kv_pidm = Column(Integer())

    sure_pidm = Column(Integer())
    kanallar_data = Column(JSON())
    sistemler_data = Column(JSON())
    dayanaklar_data = Column(JSON())
    isleme_amaclari_data = Column(JSON())
    ortamlar_data = Column(JSON())
    tedbirler_data = Column(JSON())

class ModelViewAnaveriler(FrameworkBase, _Base):
    __tablename__ = 'view_anaveriler'
    profil_pidm = Column(Integer())
    profil_name = Column(String(255))
    surec_pidm = Column(Integer())
    surec_name = Column(String(255))
    kv_pidm = Column(Integer())
    kv_name = Column(String(255))
    sure_pidm = Column(Integer())
    sure_name = Column(String(255))
    kanallar_data = Column(JSON())
    sistemler_data = Column(JSON())
    dayanaklar_data = Column(JSON())
    isleme_amaclari_data = Column(JSON())
    ortamlar_data = Column(JSON())
    tedbirler_data = Column(JSON())


# AKTARIMLAR -------------------------------------------
class ModelAktarimlar(FrameworkBase, _Base):
    __tablename__ = 'aktarimlar'
    surec_pidm = Column(Integer())
    kv_pidm = Column(Integer())
    kurum_pidm = Column(Integer())

    ulkeler_data = Column(JSON())
    dayanaklar_data = Column(JSON())
    paylasim_amaclari_data = Column(JSON())
    paylasim_sekilleri_data = Column(JSON())
    aciklama = Column(String(255))
    bilgiveren = Column(String(255))

class ModelViewAktarimlar(FrameworkBase, _Base):
    __tablename__ = 'view_aktarimlar'
    surec_pidm = Column(Integer())
    surec_name = Column(String(255))
    kv_pidm = Column(Integer())
    kv_name = Column(String(255))
    kurum_pidm = Column(Integer())
    kurum_name = Column(String(255))

    ulkeler_data = Column(JSON())
    dayanaklar_data = Column(JSON())
    paylasim_amaclari_data = Column(JSON())
    paylasim_sekilleri_data = Column(JSON())
    yurtdisi = Column(Boolean())
    aciklama = Column(String(255))
    bilgiveren = Column(String(60))

# AKTARIMLAR -------------------------------------------
class ModelTalepler(FrameworkBase, _Base):
    __tablename__ = 'talepler'
    isim = Column(String(60))
    tckno = Column(String(11))
    eposta = Column(String(100))
    tel = Column(String(30))

    dogumtarihi = Column(String(10))
    aciklama = Column(String(255))
    islem_pidm = Column(Integer())
    kurumu = Column(String(255))
    bilgitalebi = Column(String(255))
    profiller_data = Column(JSON())

class ModelViewTalepler(FrameworkBase, _Base):
    __tablename__ = 'view_talepler'
    isim = Column(String(60))
    tckno = Column(String(11))
    eposta = Column(String(100))
    tel = Column(String(30))

    dogumtarihi = Column(String(10))
    aciklama = Column(String(255))
    islem_pidm = Column(Integer())
    islem_name = Column(String(20))
    kurumu = Column(String(255))
    bilgitalebi = Column(String(255))
    profiller_data = Column(JSON())

# BOLUMLER -----------------------------------------------
class ModelBolumler(TanimlarBase, _Base):
    __tablename__ = 'bolumler'
    birim_pidm = Column(Integer())

class ModelViewBolumler(FrameworkBase, _Base):
    __tablename__ = 'view_bolumler'
    birim_pidm = Column(Integer())
    birim_name = Column(String(255))
    name = Column(String(255))


# SURECLER -----------------------------------------------
class ModelSurecler(TanimlarBase, _Base):
    __tablename__ = 'surecler'
    bolum_pidm = Column(Integer())

class ModelViewSurecler(FrameworkBase, _Base):
    __tablename__ = 'view_surecler'
    birim_name = Column(String(255))
    bolum_pidm = Column(Integer())
    bolum_name = Column(String(255))
    name = Column(String(255))

# *************** ÖZEL OPTIONS ******************************
class ModelOptions(object):
    pidm = Column(Integer(), primary_key=True)
    name = Column(String(255))
    cid = Column(Integer())

class ModelOptionsSurecler(ModelOptions,_Base):
    __tablename__ = 'options_surecler'
















