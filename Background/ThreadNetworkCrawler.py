import sys
import os

print(os.getcwd())

from Background.WebCrawler import WebCrawler

sys.path.append('../../')
from sqlalchemy import create_engine,or_,and_
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Links,Base, DomainsNetworkMetrics,get_db
import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

class ThreadNetworkCrawler:
    @staticmethod
    def retrieveDomains():
        #SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:309urje4@db:3306/debunker?"
        #SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:309urje4@localhost:9000/debunker?"

        #engine = create_engine(
        #    SQLALCHEMY_DATABASE_URL,
            #connect_args={"check_same_thread": False}
        #)

        #SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        #Base.metadata.create_all(bind=engine)

        db=next(get_db())

        current_time = datetime.datetime.utcnow()

        ten_weeks_ago = current_time - datetime.timedelta(weeks=10)
        domains_to_retrieve=db.query(DomainsNetworkMetrics).filter(or_(DomainsNetworkMetrics.overall == None,DomainsNetworkMetrics.timestamp<ten_weeks_ago)).all()
        for domain_to_retrieve in domains_to_retrieve:
            try:
                existing_links = db.query(Links).filter(
                    and_(Links.source == domain_to_retrieve.domain, Links.timestamp > ten_weeks_ago)).count()
                print(domain_to_retrieve.domain,'existing_links',existing_links)
                if existing_links > 0:
                    continue

                #remove eventually very old links
                db.query(Links).filter(
                 and_(Links.source == domain_to_retrieve.domain, Links.timestamp < ten_weeks_ago)).delete()

                edges=WebCrawler.retrieveDomains('http://'+domain_to_retrieve.domain,domain_to_retrieve.domain) #protocollo per il primo parametro?

                #insert edges in db
                for edge in edges:
                    link_model = Links()
                    link_model.source=edge[0]
                    link_model.target=edge[1]
                    link_model.weight=edge[2]
                    db.merge(link_model)
                    db.commit()
            except Exception as e:
                print('ThreadNetworkCrawler:')
                print(e)


if __name__ == "__main__":

    ThreadNetworkCrawler().retrieveDomains()