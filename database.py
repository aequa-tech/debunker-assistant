import time

from sqlalchemy import create_engine, BLOB, LargeBinary, Float, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT, LONGBLOB
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text,TIMESTAMP
from datetime import datetime





#SQLALCHEMY_DATABASE_URL = "sqlite:///./debunker.db"
#SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:309urje4@db:3306/debunker?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://debunker:A283hnd(902!)?]@db.aequa-tech.com:54321/debunker"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_recycle = 3600,
                             pool_size = 5,
                             max_overflow = 10,
                             pool_timeout = 30,
                             pool_pre_ping = True,

)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

Base = declarative_base()


class Requests(Base):
    __tablename__ = "requests"
    request_id    = Column(String(150),  primary_key=True, index=True)
    api           =  Column(String(150),  primary_key=True, index=True)
    timestamp     = Column('timestamp',  TIMESTAMP(timezone=False), primary_key=True, nullable=False, default=datetime.now())

class Urls(Base):
    __tablename__ = "urls"
    request_id    = Column(String(150), primary_key=True, index=True)
    url           = Column(Text)
    title         = Column(Text)
    content       = Column(Text)
    urls          = Column(Text)
    date          = Column(Date)
    is_reported   = Column(Integer,default=0)

class TrustableList(Base):
    __tablename__ = "trustable_list"
    domain    = Column(String(150), primary_key=True, index=True)
    source    = Column(Text,default=None)
    list_type = Column(Text,default=None) #trusted or untrusted

class DomainsLinks(Base):
    __tablename__ = "domains_links"

    source = Column(String(150), primary_key=True, index=True)
    target = Column(String(150), primary_key=True, index=True)
    weight = Column(Integer,default=0)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())

class DomainsLabelDistribution(Base):
    __tablename__ = "domains_label_distribution"

    domain    = Column(String(150), primary_key=True, index=True)
    neutral   = Column(Float,default=None)  #local numero di vicini di ordine 1 con quella label
    trusted   = Column(Float,default=None)
    untrusted = Column(Float,default=None)
    neutral_local   = Column(Float,default=None)  #local percentuale label dei vicini di ordine 1
    trusted_local   = Column(Float,default=None)
    untrusted_local = Column(Float,default=None)
    neutral_global   = Column(Float,default=None) #global distruzione della label propagation
    trusted_global   = Column(Float,default=None)
    untrusted_global = Column(Float,default=None)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())