from flask import Flask
from db.connection import Connect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, String, Integer, TIMESTAMP)
from sqlalchemy import exc
from datetime import datetime

Base = declarative_base()


class Profiller(Base):
    __tablename__ = 'profiller'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    timestamp = Column(TIMESTAMP, default = datetime.now())

class DB():
    def __init__(self):
        self.conn = Connect()
        self.session = self.conn.session()
        self.engine = self.conn.engine

    def __del__(self):
        self.session.close()

    def createBase(self):
        try:
            Base.metadata.create_all(self.engine)
        except exc.SQLAlchemyError:
            print("DB Error ", exc)


if __name__ == "__main__":
    db = DB()
    db.createBase()

    # print("Base created successfully..")