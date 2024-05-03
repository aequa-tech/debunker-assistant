import time

from sqlalchemy import create_engine, BLOB, LargeBinary, Float, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT, LONGBLOB
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text,TIMESTAMP
from datetime import datetime





SQLALCHEMY_DATABASE_URL = "sqlite:///./debunker.db"
#SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:309urje4@db:3306/debunker?charset=utf8mb4"
#SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:8889/debunker?charset=utf8mb4"

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

class Urls(Base):
    __tablename__ = "urls"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_general_ci'}

    request_id = Column(String(150), primary_key=True, index=True)
    url = Column(Text)
    title = Column(Text)
    content = Column(Text)
    date = Column(Date)
    is_reported = Column(Integer,default=0)


class DomainsLabelDistribution(Base):
    __tablename__ = "domains_label_distribution"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_general_ci'}

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


class DomainsWhois(Base):
    __tablename__ = "domains_whois"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_general_ci'}

    domain = Column(String(150), primary_key=True, index=True)
    overall = Column(Float,default=None)
    registrant_country = Column(Text,default=None)
    creation_date = Column(DateTime,default=None)
    expiration_date = Column(DateTime,default=None)
    last_updated = Column(DateTime,default=None)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())


class DomainsNetworkMetrics(Base):
    __tablename__ = "domains_network_metrics"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_general_ci'}

    domain = Column(String(150), primary_key=True, index=True)
    overall=Column(Float,default=None)
    pagerank=Column(Float,default=None)
    closeness=Column(Float,default=None)
    betweenness=Column(Float,default=None)
    hub=Column(Float,default=None)
    authority = Column(Float,default=None)
    degree_in = Column(Integer,default=None)
    degree_out = Column(Integer,default=None)
    neighborhood_list= Column(Text,default=None)
    white_community = Column(Float,default=None)
    black_community = Column(Float,default=None)
    white_list= Column(Text,default=None)
    black_list= Column(Text,default=None)
    is_blacklist=Column(Float,default=None)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())

class List(Base):
    __tablename__ = "list"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_general_ci'}

    domain    = Column(String(150), primary_key=True, index=True)
    source    = Column(Text,default=None)
    list_type = Column(Text,default=None) #white or black

class Links(Base):
    __tablename__ = "links"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_general_ci'}

    source = Column(String(150), primary_key=True, index=True)
    target = Column(String(150), primary_key=True, index=True)
    weight = Column(Integer,default=0)
    timestamp = Column('timestamp', TIMESTAMP(timezone=False), nullable=False, default=datetime.now())