from sqlalchemy import (Column, String, Integer, TIMESTAMP, Boolean, JSON)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

# _Base tek _ underscore private olduğu ve  dışardan import edilemeyeceği anlamnıa geliyor.
# tek _ classlar için, __ çifti tanım ve fonksiyonlar için
_Base = declarative_base()


# react tarafından post edilen ID'leri tek noktadan kolayca yönetebilmek için yazıldı.
class ModelID():
    Profiller = ["profil", "profiller"]
    Birimler = ["birim", "birimler"]
    Bolumler = ["bolum", "bolumler"]
    Surecler = ["surec", "surecler"]
    KV = ["kv"]
    Sorumlular = ["sorumlular"]
    Dayanaklar = ["dayanaklar"]
    Sureler = ["sure", "sureler"]
    IslemeAmaclari = ["isleme_amaclari"]
    ToplamaKanallari = ["kanallar"]
    Kurumlar = ["kurumlar"]
    KVKategoriler = ["kv_kategoriler"]
    ArsivOrtamlari = ["ortamlar"]
    PaylasimAmaclari = ["paylasim_amaclari"]
    PaylasimSekilleri = ["paylasim_sekilleri"]
    KVSistemler = ["sistemler"]
    GuvenliUlkeler = ["ulkeler"]
    Islemler = ["islemler"]
    Tedbirler = ["tedbirler"]
    Anaveriler = ["anaveriler"]
    Aktarimlar = ["aktarimlar"]
    Talepler = ["talepler"]


def getModel(id):
    if (id in ModelID.Profiller):
        model = ModelProfiller
    elif (id in ModelID.Birimler):
        model = ModelBirimler
    elif (id in ModelID.Dayanaklar):
        model = ModelDayanaklar
    elif (id in ModelID.IslemeAmaclari):
        model = ModelIslemeAmaclari
    elif (id in ModelID.ToplamaKanallari):
        model = ModelKanallar
    elif (id in ModelID.KV):
        model = ModelKV
    elif (id in ModelID.KVKategoriler):
        model = ModelKVKategoriler
    elif (id in ModelID.ArsivOrtamlari):
        model = ModelOrtamlar
    elif (id in ModelID.KVSistemler):
        model = ModelSistemler
    elif (id in ModelID.Sureler):
        model = ModelSureler
    elif (id in ModelID.Kurumlar):
        model = ModelKurumlar
    elif (id in ModelID.PaylasimAmaclari):
        model = ModelPaylasimAmaclari
    elif (id in ModelID.PaylasimSekilleri):
        model = ModelPaylasimSekilleri
    elif (id in ModelID.GuvenliUlkeler):
        model = ModelUlkeler
    elif (id in ModelID.Islemler):
        model = ModelIslemler
    elif (id in ModelID.Tedbirler):
        model = ModelTedbirler
    elif (id in ModelID.Anaveriler):
        model = ModelAnaveriler
    elif (id in ModelID.Aktarimlar):
        model = ModelAktarimlar
    elif (id in ModelID.Talepler):
        model = ModelTalepler
    elif (id in ModelID.Sorumlular):
        model = ModelSorumlular
    else:
        model = None

    return model

# özel optionslar için...


def getOptionsModel(id):
    if (id in ModelID.Surecler):
        model = ModelOptionsSurecler
    elif (id in ModelID.Profiller):
        model = ModelProfiller
    elif (id in ModelID.Bolumler):
        model = ModelOptionsBolumler
    elif (id in ModelID.Birimler):
        model = ModelBirimler
    elif (id in ModelID.Dayanaklar):
        model = ModelDayanaklar
    elif (id in ModelID.IslemeAmaclari):
        model = ModelIslemeAmaclari
    elif (id in ModelID.ToplamaKanallari):
        model = ModelKanallar
    elif (id in ModelID.KV):
        model = ModelKV
    elif (id in ModelID.KVKategoriler):
        model = ModelKVKategoriler
    elif (id in ModelID.ArsivOrtamlari):
        model = ModelOrtamlar
    elif (id in ModelID.KVSistemler):
        model = ModelSistemler
    elif (id in ModelID.Sureler):
        model = ModelSureler
    elif (id in ModelID.Kurumlar):
        model = ModelKurumlar
    elif (id in ModelID.PaylasimAmaclari):
        model = ModelPaylasimAmaclari
    elif (id in ModelID.PaylasimSekilleri):
        model = ModelPaylasimSekilleri
    elif (id in ModelID.GuvenliUlkeler):
        model = ModelUlkeler
    elif (id in ModelID.Islemler):
        model = ModelIslemler
    elif (id in ModelID.Tedbirler):
        model = ModelTedbirler
    elif (id in ModelID.Sorumlular):
        model = ModelSorumlular
    else:
        # diğer optionsları getModelden alıyor.. burası özel options için
        model = None

    return model


# TANIMLAR ********************************************************
# Custom base class

class ModelBase(object):
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
    __tablename__ = 't_profiller'


class ModelDayanaklar(TanimlarBase, _Base):
    __tablename__ = 't_dayanaklar'


class ModelKVKategoriler(TanimlarBase, _Base):
    __tablename__ = 't_kv_kategoriler'


class ModelIslemeAmaclari(TanimlarBase, _Base):
    __tablename__ = 't_isleme_amaclari'


class ModelKanallar(TanimlarBase, _Base):
    __tablename__ = 't_kanallar'


class ModelOrtamlar(TanimlarBase, _Base):
    __tablename__ = 't_ortamlar'


class ModelSureler(TanimlarBase, _Base):
    __tablename__ = 't_sureler'


class ModelKurumlar(TanimlarBase, _Base):
    __tablename__ = 't_kurumlar'


class ModelPaylasimAmaclari(TanimlarBase, _Base):
    __tablename__ = 't_paylasim_amaclari'


class ModelPaylasimSekilleri(TanimlarBase, _Base):
    __tablename__ = 't_paylasim_sekilleri'


# KV TALEPLER Tablosu için
class ModelIslemler(TanimlarBase, _Base):
    __tablename__ = 't_islemler'


class ModelTedbirler(TanimlarBase, _Base):
    __tablename__ = 't_tedbirler'


class ModelCid(_Base):
    __tablename__ = 't_cid'
    pidm = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ModelAuth(_Base):
    __tablename__ = 'auth'
    pidm = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    dpo = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    enabled = Column(Boolean, default=False)
    cid_data = Column(JSON())
    timestamp = Column(TIMESTAMP, default=datetime.now())
    uid = Column(String)


class ModelViewAuth(_Base):
    __tablename__ = 'view_auth'
    # SQLAlchemt her tabloda primary_key istediği için eklendi
    rownumber = Column(Integer, primary_key=True)  # edit de unique satırı yakalamak için generate ediliyor. 
    pidm = Column(Integer)
    username = Column(String)
    password = Column(String)
    cid = Column(Integer)
    cid_name = Column(String)
    dpo = Column(Boolean)
    admin = Column(Boolean)
    enabled = Column(Boolean)
    uid = Column(String)


class ModelTalepler(ModelBase, _Base):
    __tablename__ = 'v_talepler'
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


class ModelViewTalepler(ModelBase, _Base):
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
    __tablename__ = 't_bolumler'
    birim_pidm = Column(Integer())


class ModelViewBolumler(ModelBase, _Base):
    __tablename__ = 'view_bolumler'
    birim_pidm = Column(Integer())
    birim_name = Column(String(255))
    name = Column(String(255))


# SURECLER -----------------------------------------------
class ModelSurecler(TanimlarBase, _Base):
    __tablename__ = 't_surecler'
    bolum_pidm = Column(Integer())


class ModelViewSurecler(TanimlarBase, _Base):
    __tablename__ = 'view_surecler'
    birim_name = Column(String(255))
    bolum_pidm = Column(Integer())
    bolum_name = Column(String(255))


# KV -------------------------------------------
class ModelKV(TanimlarBase, _Base):
    __tablename__ = 't_kv'
    kv_kategori_pidm = Column(Integer())


class ModelViewKV(TanimlarBase, _Base):
    __tablename__ = 'view_kv'
    kv_kategori_pidm = Column(Integer())
    kv_kategori_name = Column(String(255))


# *************** ÖZEL OPTIONS ******************************
class ModelOptions(object):
    pidm = Column(Integer(), primary_key=True)
    name = Column(String(255))
    cid = Column(Integer())


class ModelOptionsBolumler(ModelOptions, _Base):
    __tablename__ = 'options_bolumler'


class ModelOptionsSurecler(ModelOptions, _Base):
    __tablename__ = 'options_surecler'


class ModelUlkeler(TanimlarBase, _Base):
    __tablename__ = 't_ulkeler'
    phone_area = Column(String(3))
    secure = Column(Boolean())


class ModelViewUlkeler(TanimlarBase, _Base):
    __tablename__ = 'view_ulkeler'
    phone_area = Column(String(3))
    secure = Column(Boolean())


class ModelSistemler(TanimlarBase, _Base):
    __tablename__ = 't_sistemler'
    local = Column(Boolean())


class ModelViewSistemler(TanimlarBase, _Base):
    __tablename__ = 'view_sistemler'
    local = Column(Boolean())


class ModelBirimler(TanimlarBase, _Base):
    __tablename__ = 't_birimler'
    sorumlular_data = Column(JSON())

# Birimler > Veri sorumluları


class ModelViewBirimler(TanimlarBase, _Base):
    __tablename__ = 'view_birimler'
    sorumlular_data = Column(JSON())


class ModelSorumlular(TanimlarBase, _Base):
    __tablename__ = 't_sorumlular'
    phone = Column(String(100))
    email = Column(String(100))


class ModelKisiler(TanimlarBase, _Base):
    __tablename__ = 't_kisiler'
    profiller_data = Column(JSON())
    birimler_data = Column(JSON())
    kimlikno = Column(String(11))
    tel = Column(String(100))
    eposta = Column(String(100))

# ************* CHARTS *****************************


class ModelChartTalepler(_Base):
    __tablename__ = 'chart_talepler'
    name = Column(String(100), primary_key=True)
    value = Column(Integer())
    cid = Column(Integer())


class ModelTree(object):
    name = Column(String(100), primary_key=True)
    data = Column(JSON())
    cid = Column(Integer())


class ModelChartTreeBirimKV(ModelTree, _Base):
    __tablename__ = 'chart_tree_birimkv'


class ModelChartTreeProfilKV(ModelTree, _Base):
    __tablename__ = 'chart_tree_profilkv'


class ModelChartTreeBirimKurum(ModelTree, _Base):
    __tablename__ = 'chart_tree_birimkurum'


class ModelChartMap(_Base):
    __tablename__ = 'chart_map'
    name = Column(String(255), primary_key=True)
    value = Column(Integer())
    cid = Column(Integer())


class ModelViewBirimBolumler(_Base):
    __tablename__ = 'view_birim_bolumler'
    birim_name = Column(String, primary_key=True)
    bolumler_data = Column(JSON())
    cid = Column(Integer())


class ModelViewBolumSurecler(_Base):
    __tablename__ = 'view_bolum_surecler'
    birim_name = Column(String, primary_key=True)
    bolum_name = Column(String, primary_key=True)
    surecler_data = Column(JSON())
    cid = Column(Integer())


# ENVANTER **********************************************
class BaseEnvanter(object):
    pidm = Column(Integer(), primary_key=True)
    data = Column(JSON())
    timestamp = Column(TIMESTAMP, default=datetime.now())
    cid = Column(Integer())
    uid = Column(String(100))


class ModelAnaveriler(BaseEnvanter, _Base):
    __tablename__ = 'v_anaveriler2'


class ModelAktarimlar(BaseEnvanter, _Base):
    __tablename__ = 'v_aktarimlar2'



