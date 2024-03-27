import sys

sys.path.append('../../')
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Links, Base, Urls, DomainsWhois, get_db
import requests
import datetime
import whois
import time


class ThreadWhoIs:
    @staticmethod
    def retrieveDomains():
        #SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:309urje4@db:3306/debunker?"

        #engine = create_engine(
        #    SQLALCHEMY_DATABASE_URL,
            # connect_args={"check_same_thread": False}
        #)

        #SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        #Base.metadata.create_all(bind=engine)

        db=next(get_db())

        current_time = datetime.datetime.utcnow()

        ten_weeks_ago = current_time - datetime.timedelta(weeks=10)
        domains_to_retrieve = db.query(DomainsWhois).filter(
            or_(DomainsWhois.overall == None, DomainsWhois.timestamp < ten_weeks_ago)).all()
        # @urbinati, ragionare meglio l'overall sul parametro solidity
        for domain_to_retrieve in domains_to_retrieve:
            try:
                time.sleep(2)
                print(domain_to_retrieve.domain)
                w = whois.query(domain_to_retrieve.domain)
                if w.registrant_country == '':
                    w.registrant_country = 'N/D'
                domain_to_retrieve.registrant_country = w.registrant_country
                domain_to_retrieve.creation_date = w.creation_date
                domain_to_retrieve.expiration_date = w.expiration_date
                domain_to_retrieve.last_updated = w.last_updated

                if w.creation_date is None or w.last_updated is None:
                    overall = None
                else:

                    days_since_creation = (current_time - w.creation_date).days
                    days_since_last_update = (current_time - w.last_updated).days

                    if days_since_creation >= (5 * 365) and days_since_last_update >= (365):
                        overall = 1
                    elif days_since_creation >= (5 * 365) and days_since_last_update < (365):
                        overall = 0.75
                    elif days_since_creation < (5 * 365) and days_since_last_update >= (365):
                        overall = 0.50
                    elif days_since_creation < (5 * 365) and days_since_last_update < (365):
                        overall = 0.25

                domain_to_retrieve.overall = overall
                db.commit()
            except Exception as e:
                print('ThreadWhoIs: ',domain_to_retrieve.domain)
                print(e)
                continue



if __name__ == "__main__":
    ThreadWhoIs().retrieveDomains()
    w = whois.query('pianetablunews.it')
    print(w.tld)
    print(w.registrant_country)
    print(w.abuse_contact)
    print(w.statuses)
    print(w.registrant)
    print(w.dnssec)
    current_time = datetime.datetime.utcnow()
    print(w.last_updated)
    days_since_creation = (current_time - w.last_updated).days
    print(days_since_creation)