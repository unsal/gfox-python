from sqlalchemy import (Column, String, Integer, TIMESTAMP)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profiller(Base):
    __tablename__ = 'profiller'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default = datetime.now())

class Birimler(Base):
    __tablename__ = 'birimler'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.now())



