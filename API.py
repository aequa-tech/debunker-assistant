import json
from urllib.parse import urlparse
import numpy
from sqlalchemy.exc import IntegrityError
import uvicorn

from features.nlp.Scores import InformalStyle, ClickBait, Readability
from webScraper.WebScraper import WebScraper
import hashlib
from fastapi import FastAPI, Depends
from database import engine, SessionLocal,Base,Urls,DomainsWhois, DomainsNetworkMetrics, get_db
from sqlalchemy.orm import Session
from datetime import datetime, time,timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware



from Background.ThreadNetworkCrawler import ThreadNetworkCrawler
from Background.ThreadNetworkMetrics import ThreadNetworkMetrics
from Background.ThreadWhoIs import ThreadWhoIs
"""from fastapi_utils.tasks import repeat_every"""


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

informalStyle = InformalStyle()
clickBait = ClickBait()
readability = Readability()
apis = {
    'informal_style' : {
         'use_of_first_and_second_person' : informalStyle.use_of_first_and_second_person,
         'use_of_personal_style' : informalStyle.use_of_personal_style,
         'use_of_intensifier_score' : informalStyle.use_of_intensifier_score,
         'use_of_shorten_form_score' : informalStyle.use_of_shorten_form_score,
         'use_of_modals_score' : informalStyle.use_of_modals_score,
         'use_of_interrogative_score' : informalStyle.use_of_interrogative_score,
         'use_of_uppercase_words' : informalStyle.use_of_uppercase_words,
         'use_of_repeated_letters' : informalStyle.use_of_repeated_letters,
         'use_of_aggressive_punctuation' : informalStyle.use_of_aggressive_punctuation,
         'use_of_uncommon_punctuation' : informalStyle.use_of_uncommon_punctuation,
         'use_of_emoji' : informalStyle.use_of_emoji,
    },
    "readability" : {
         'flesch_reading_ease': readability.flesch_reading_ease,
    },
    "clickbait" : {
         'misleading_headline': clickBait.misleading_headline,
    },

}


@app.post("/api/v2/scrape")
async def retrieveUrl(url : str, db: Session = Depends(get_db)):
    hash_id = hashlib.md5(url.encode('utf-8')).hexdigest()
    url_object=db.query(Urls).filter(Urls.request_id == hash_id).first()
    if url_object is None:
        webScraper=WebScraper()
        result=webScraper.scrape(url)
        jsonResult=json.loads(result)

        if jsonResult['status'] == 200:
            url_model = Urls()
            url_model.url          = url
            url_model.title        = jsonResult['result']['title']
            url_model.content  = jsonResult['result']['content'].replace('\n',' ')
            url_model.date         = datetime.strptime(jsonResult['result']['date'], '%Y-%M-%d')
            url_model.request_id   = hash_id
            db.add(url_model)
            db.commit()
            jsonResult['result']['request_id'] = hash_id


        return  jsonResult


    else:

        # result=db.query(DomainsWhois).filter(DomainsWhois.domain==tldextract.extract(url).registered_domain).first()
        result = db.query(DomainsWhois).filter(DomainsWhois.domain == urlparse(url).netloc).first()
        print(result)
        if result is None:
            domains_whois_model = DomainsWhois()
            domains_whois_model.domain = urlparse(url).netloc  # tldextract.extract(url).registered_domain
            db.add(domains_whois_model)
            db.commit()
            print("inserted DomainsWhois", urlparse(url).netloc)
        # result=db.query(DomainsNetworkMetrics).filter(DomainsNetworkMetrics.domain==tldextract.extract(url).registered_domain).first()
        result = db.query(DomainsNetworkMetrics).filter(DomainsNetworkMetrics.domain == urlparse(url).netloc).first()
        print(result)
        if result is None:
            domains_network_metrics = DomainsNetworkMetrics()
            domains_network_metrics.domain = urlparse(url).netloc  # tldextract.extract(url).registered_domain
            db.add(domains_network_metrics)
            db.commit()
            print("inserted DomainsNetworkMetrics", urlparse(url).netloc)

        return {'status':200,
                'message':'the request was successful',
                'result': {
                        'request_id':url_object.request_id,
                        'status':200,
                        'title':url_object.title,
                        'content': url_object.content,
                        'date': datetime.strftime(url_object.date, '%Y-%M-%d'),
                        'is_reported':url_object.is_reported
                        }
                }



@app.get("/api/v2/report_url/{request_id}")
async def getReportUrl(request_id : str, db: Session = Depends(get_db)):
    url_object=db.query(Urls).filter(Urls.request_id == request_id).first()

    if url_object is not None:
        url_object.is_reported=1
        db.commit()


        return { 'status': 200, 'message': 'url has been successfully reported'}
    else:
        return { 'status': 400, 'message': 'request_id unavailable'}


@app.post("/api/v2/report_domain")
async def getReportDomain(url : str, db: Session = Depends(get_db)):
    webScraper = WebScraper()
    result = webScraper.scrape(url)
    jsonResult = json.loads(result)

    if jsonResult['status'] == 200:

        try:
            result=db.query(DomainsWhois).filter(DomainsWhois.domain==urlparse(url).netloc).first()
            if result is None:
                print('reported DomainsWhois',urlparse(url).netloc)
                domains_whois_model = DomainsWhois()
                domains_whois_model.domain = urlparse(url).netloc#tldextract.extract(url).registered_domain
                db.add(domains_whois_model)
                db.commit()

            result=db.query(DomainsNetworkMetrics).filter(DomainsNetworkMetrics.domain==urlparse(url).netloc).first()
            if result is None:
                print('reported DomainsNetworkMetrics',urlparse(url).netloc)
                domains_network_metrics = DomainsNetworkMetrics()
                domains_network_metrics.domain = urlparse(url).netloc#tldextract.extract(url).registered_domain
                db.add(domains_network_metrics)
                db.commit()

            return { 'status': 200, 'message': 'domain has been successfully reported'}
        except IntegrityError:
            return { 'status': 500, 'message': 'IntegrityError'}
    else:
        return {'status': 400, 'message': 'the domain is not available or does not exist'}


@app.get("/api/v1/available_domains/{page}/{page_size}")
async def getAvailableDomains(page: int, page_size: int, db: Session = Depends(get_db)):

    print(page,page_size)
    domains = db.query(DomainsWhois).order_by(DomainsWhois.domain.asc()).offset(page*page_size).limit(page_size)
    print(domains)

    return { 'status': 200,
                 'message': 'the request was successful (random values)',
                 'result': {
                             'urls': [domain.domain for domain in domains ]
                        }
           }

@app.get("/api/v1/available_urls/{page}/{page_size}")
async def getAvailableUrls(page: int, page_size: int, db: Session = Depends(get_db)):

    print(page,page_size)
    urls = db.query(Urls).order_by(Urls.url.asc()).offset(page*page_size).limit(page_size)
    print(urls)

    return { 'status': 200,
                 'message': 'the request was successful (random values)',
                 'result': {
                             'urls': [url.url for url in urls ]
                        }
           }

@app.get("/api/v2/{group}/{phenomenon}/{request_id}")
async def getGeneralAPI(group : str, phenomenon : str, request_id : str, db: Session = Depends(get_db)):
    url_object=db.query(Urls).filter(Urls.request_id == request_id).first()
    if url_object is not None:

        res = apis[group][phenomenon](url_object.title,url_object.content)

        return { 'status': 200, 'message':'the request was successful', 'result': res  }

    else:

        return {'status':400,'message':'request_id not available. Recover the content of the url by /api/v2/scrape first.'}

@app.get("/api/v2/{group}/{request_id}")
async def getGeneralAggregateAPIs(group : str, request_id : str, db: Session = Depends(get_db)):
    url_object=db.query(Urls).filter(Urls.request_id == request_id).first()
    result={}
    result["description"]={
                                "en": f"Aggregation of {group.replace('_',' ')} features.",
                                "it": "descrizione in italiano"
                          }

    if url_object is not None:

        overall_title   = []
        overall_content = []
        result['disaggregated']={}
        for key, value in apis[group].items():
            res = value(url_object.title,url_object.content)
            overall_title.append(res['title']['values']['local_normalisation'])
            overall_content.append(res['content']['values']['local_normalisation'])
            result['disaggregated'][key]=res.copy()

        result['title']   = { 'overall'  :numpy.average(overall_title) }
        result['content'] = { 'overall':numpy.average(overall_content) }

        return { 'status': 200, 'message':'the request was successful', 'result': result  }

    else:

        return {'status':400,'message':'request_id not available. Recover the content of the url by /api/v2/scrape first.'}




scheduler=BackgroundScheduler()
def NetworkCrawler():
    print("Starting background processes")

    ThreadNetworkCrawler().retrieveDomains()

    ThreadWhoIs().retrieveDomains()

    ThreadNetworkMetrics().retrieveDomains()




tomorrow_start = datetime.combine(datetime.today(), time(0, 0)) + timedelta(1)

scheduler.add_job(NetworkCrawler, 'interval', hours=24,max_instances=1,next_run_time=tomorrow_start)
#scheduler.add_job(NetworkCrawler, 'interval', minutes=1,max_instances=1)#,next_run_time=tomorrow_start)
scheduler.start()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)