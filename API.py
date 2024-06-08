import numpy as np
import uvicorn
from fastapi import FastAPI, Depends, Response, status
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, Urls, get_db, Requests
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import numpy
import hashlib
import json
from datetime import datetime, time,timedelta
import uuid
from urllib.parse import urlparse

from News import News

from features.nlp.affective import Sentiment, Emotion
from features.nlp.danger    import Irony, Flame, Stereotype
from features.nlp.scores    import InformalStyle, ClickBait, Readability
from features.na.Network    import Network

from explainability.explainer import Affective,Danger

#from apscheduler.schedulers.background import BackgroundScheduler
#from Background.ThreadNetworkCrawler   import ThreadNetworkCrawler
#from Background.ThreadNetworkMetrics   import ThreadNetworkMetrics
#from Background.ThreadWhoIs import ThreadWhoIs


basePath="/internal/v1/"

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
sentiment = Sentiment()
emotion = Emotion()
irony = Irony()
flame = Flame()
stereotype = Stereotype()
network = Network()
exp_danger = Danger()
exp_affective = Affective()

apis = {
    'informalStyle' : {
         'secondPerson' : informalStyle.use_of_first_and_second_person,
         'personalStyle' : informalStyle.use_of_personal_style,
         'intensifiers' : informalStyle.use_of_intensifier_score,
         'shortenedForms' : informalStyle.use_of_shorten_form_score,
         'modals' : informalStyle.use_of_modals_score,
         'interrogatives' : informalStyle.use_of_interrogative_score,
         'uppercaseWords' : informalStyle.use_of_uppercase_words,
         'repeatedLetters' : informalStyle.use_of_repeated_letters,
         'aggressivePunctuation' : informalStyle.use_of_aggressive_punctuation,
         'uncommonPunctuation' : informalStyle.use_of_uncommon_punctuation,
         'emoji' : informalStyle.use_of_emoji,
    },
    "readability" : {
         'fleshReadingEase': readability.flesch_reading_ease,
    },
    "clickBait" : {
         'misleadingHeadline': clickBait.misleading_headline,
    },
    "affectiveStyle" : {
         'joy': emotion.get_emotion_joy,
         'sadness': emotion.get_emotion_sadness,
         'fear': emotion.get_emotion_fear,
         'anger': emotion.get_emotion_anger,
         'positiveSentiment': sentiment.get_sentiment_positive,
         'negativeSentiment': sentiment.get_sentiment_negative,
    },
    "dangerousStyle" : {

        'irony': irony.get_irony,
        'flame': flame.get_flame,
        'stereotype': stereotype.get_stereotype,

    },
    "untrustability": {

        'labelPropagation': network.get_backpropagation_untrustability,

    },
    "explanations": {
        "explanationDanger": exp_danger.danger_explanation,
        "explanationAffective": exp_affective.affective_explanation,


    }
}


@app.post(basePath+"scrape",status_code=status.HTTP_200_OK,description='retrieve the title and the body of an article')
async def api_scrape(inputUrl   : str = None,
                     language   : str = "en",
                     retry      : str = False,
                     maxRetries : str = 5,
                     timeout    : str = 10,
                     maxChars   : str = 10000,
                 db: Session = Depends(get_db),
                 response = Response):

    if inputUrl is None:
        message = 'bad request'
        return response(content=message,status_code=status.HTTP_400_BAD_REQUEST)

    hash_id = hashlib.md5(inputUrl.encode('utf-8')).hexdigest()

    #inizio memorizzazione la richiesta:
    """potremmo pensare di salvare anche l'IP del richiedente"""
    request=Requests()
    request.request_id=hash_id
    request.api="scrape"
    request.timestamp=datetime.now()
    db.add(request)
    db.commit()
    #fine memorizzazione della richiests

    #inizio verifica dei parametri:
    """dobbiamo:
    - verificare che i paramentri obbligatori siano presenti
    - verificare che i valori siano ammissibili
    - scrivere dei messaggi d'errore a seconda del parametro mancante o con valori non ammessi"""


    if language is None:
        language="en"
    elif language not in ["it","en"]:
        message = "bad request"
        return response(content=message, status_code=status.HTTP_400_BAD_REQUEST,media_type='text')


    
    #fine verifica dei parametri


    #inizio verifica se l'articolo è già in db
    url_object=db.query(Urls).filter(Urls.request_id == hash_id).first()

    #caso 1: l'articolo è già in db
    if url_object is not None:

        result = {'request_id':url_object.request_id,
                        }


        return response(content=json.dumps(result),status_code=status.HTTP_200_OK)
    
    #caso 2: l'articolo non è in db, è necessario recuperarlo
    else:
        webScraper=News()
        result=webScraper.get_news_from_url(inputUrl)
        jsonResult=json.loads(result)

        if jsonResult['status'] == 200:
            url_model = Urls()
            url_model.request_id   = hash_id
            url_model.url          = inputUrl
            url_model.title        = jsonResult['result']['title'][0:maxChars]
            url_model.content      = jsonResult['result']['content'][0:maxChars]
            url_model.date         = datetime.strptime(jsonResult['result']['date'], '%Y-%M-%d')
            url_model.urls         = json.dumps(jsonResult['result']['urls'])
            db.add(url_model)
            db.commit()
            #jsonResult['result']['request_id'] = hash_id
            result = {'request_id':url_model.request_id,
                        }


            return response(content=json.dumps(result),status_code=status.HTTP_200_OK)
    
        else:
            message = "we didn't find the page that you requested"
            return response(content=message,status_code=status.HTTP_400_BAD_REQUEST)



@app.post(basePath+"internal/scrape")
async def api_scrape(inputUrl   : str = None,
                     language   : str = "en",
                     retry      : str = None,
                     maxRetries : str = None,
                     timeout    : str = None,
                     maxChars   : str = None,
                 db: Session = Depends(get_db)):

    if inputUrl is None:
        return {'status': 400}

    hash_id = hashlib.md5(inputUrl.encode('utf-8')).hexdigest()

    #inizio memorizzazione la richiesta:
    """potremmo pensare di salvare anche l'IP del richiedente"""
    request=Requests()
    request.request_id=hash_id
    request.api="scrape"
    request.timestamp=datetime.now()
    db.add(request)
    db.commit()
    #fine memorizzazione della richiests

    #inizio verifica dei parametri:
    """dobbiamo:
    - verificare che i paramentri obbligatori siano presenti
    - verificare che i valori siano ammissibili
    - scrivere dei messaggi d'errore a seconda del parametro mancante o con valori non ammessi"""


    if language is None:
        language="en"
    elif language not in ["it","en"]:
        return {'status': 400}

    maxChars=10000
    #fine verifica dei parametri


    #inizio verifica se l'articolo è già in db
    url_object=db.query(Urls).filter(Urls.request_id == hash_id).first()

    #caso 1: l'articolo è già in db
    if url_object is not None:


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
    #caso 2: l'articolo non è in db, è necessario recuperarlo
    else:
        webScraper=News()
        result=webScraper.get_news_from_url(inputUrl)
        jsonResult=json.loads(result)

        if jsonResult['status'] == 200:
            url_model = Urls()
            url_model.request_id   = hash_id
            url_model.url          = inputUrl
            url_model.title        = jsonResult['result']['title'][0:maxChars]
            url_model.content      = jsonResult['result']['content'][0:maxChars]
            url_model.date         = datetime.strptime(jsonResult['result']['date'], '%Y-%M-%d')
            url_model.urls         = json.dumps(jsonResult['result']['urls'])
            db.add(url_model)
            db.commit()
            jsonResult['result']['request_id'] = hash_id
        return  jsonResult



@app.get(basePath+"evaluation",status_code=status.HTTP_200_OK,description="""the output of this API call is a json in which 
         outputs are organized in three levels. It is possible to find all dimensions of evaluation (eg: 'informal style') and 
         all the features that contribute to determine them (eg: the presence of exclamation marks in a title).""")
async def article_evaluation (language : str = "en",
                 request_id   : str = None,
                 db: Session = Depends(get_db),
                 response = Response):

    #inizio memorizzazione la richiesta:
    """potremmo pensare di salvare anche l'IP del richiedente"""
    request=Requests()
    request.request_id=request_id
    request.api="evaluation"
    request.timestamp=datetime.now()
    db.add(request)
    db.commit()
    #fine memorizzazione della richiests

    #inizio verifica dei parametri:
    """dobbiamo:
    - verificare che i paramentri obbligatori siano presenti
    - verificare che i valori siano ammissibili
    - scrivere dei messaggi d'errore a seconda del parametro mancante o con valori non ammessi"""
    if request_id is None:
        message = "bad request"
        return response(content=message,status_code=status.HTTP_400_BAD_REQUEST)
    #fine verifica dei parametri


    #inizio verifica se l'articolo è già in db
    url_object=db.query(Urls).filter(Urls.request_id == request_id).first()
    if url_object is None:
        message = 'forbidden request'
        return response(content=message,status_code=status.HTTP_403_FORBIDDEN)
    #fine verifica se l'articolo è già in db


    content={"analysisId": request_id, #per ora ho messo lo stesso di request_id
              "informalStyle": await getGeneralAggregateAPIs(language,"informalStyle",request_id,db),
              "readability":  await getGeneralAggregateAPIs(language,"readability",request_id,db),
              "clickBait":  await getGeneralAggregateAPIs(language,"clickBait",request_id,db),
              "affectiveStyle":  await getGeneralAggregateAPIs(language,"affectiveStyle",request_id,db),
              "dangerousStyle":  await getGeneralAggregateAPIs(language,"dangerousStyle",request_id,db),
              "untrustability":  await getGeneralAggregateAPIs(language,"untrustability",request_id,db),
            }

    if content['untrustability'] is None:
        return response(content=json.dumps(content),status_code=status.HTTP_206_PARTIAL_CONTENT)
    else:
        return response(content=json.dumps(content))


@app.get(basePath+"explanations",status_code=status.HTTP_200_OK,description="""the output of these api is an explanation related to
          a given set of predictions. With explanation we mean the piece of text that contributes the most to the classification""")
async def explanation(analysis_id : str, explanation_type : str, language : str = "en",
                      db: Session = Depends(get_db),
                      response = Response):
    ### how to get the evaluation_id from the db?
    request=Requests()
    request.request_id=analysis_id
    request.api="explanations"
    request.timestamp=datetime.now()
    db.add(request)
    db.commit()

    url =db.query(Urls).filter(Urls.request_id == analysis_id).first()
    title=url.title
    content=url.content
    if explanation_type == 'explanationDanger':
        content = apis['explanations'][explanation_type](title, content, language)
    elif explanation_type == 'explanationAffective':
        content = apis['explanations'][explanation_type](title, content, language)
    else:
        return response(content="Avaluation type not available",status_code=status.HTTP_200_OK)

    return response(content=json.dumps(content))

@app.get(basePath+"{language}/{group}/{request_id}")
async def getGeneralAggregateAPIs(language, group : str, request_id : str, db: Session = Depends(get_db)):
    url_object=db.query(Urls).filter(Urls.request_id == request_id).first()
    result={}

    descriptions= {"en": f"Aggregation of {group.replace('_',' ')} features.",
                    "it": "descrizione in italiano"}

    result["description"]=descriptions[language]

    if url_object is not None:
        if group in apis.keys():

            if group == "untrustability": # le API di tipo network sono particolari

                overall   = []
                result['disaggregated']={}
                for key, value in apis[group].items():
                    res = value(url_object.url,db)
                    if res is None:
                        return None
                    else:
                        print(res)
                        overall.append(res['values']['local'])
                        result['disaggregated'][key]=res.copy()

                result['overallScore'] = numpy.average(overall)

                return result

            else:
                overall_title   = []
                overall_content = []
                result['disaggregated']={}
                for key, value in apis[group].items():
                    res = value(language,url_object.title,url_object.content)
                    print(key, value)
                    print(res)
                    overall_title.append(res['title']['values']['local'])
                    overall_content.append(res['content']['values']['local'])
                    result['disaggregated'][key]={ 'title'  :res['title']['values'],
                                                   'content':res['content']['values'] }

                result['overallScore']   = { 'title'  :numpy.average(overall_title),
                                             'content':numpy.average(overall_content) }

                return result

        else:
            return {'status': 500, 'message': 'Endpoint not available'}

    else:
        return {'status':400,'message':'request_id not available. Recover the content of the url by /api/v2/scrape first.'}

@app.get(basePath+"{language}/{group}/{phenomenon}/{request_id}")
async def getGeneralAPI(language,group : str, phenomenon : str, request_id : str, db: Session = Depends(get_db)):

    if group in apis.keys():

        if group == "untrustability": #le API di tipo network sono particolari

            url_object = db.query(Urls).filter(Urls.request_id == request_id).first()
            if url_object is not None:
                res = network.get_backpropagation_untrustability(url_object.url, db)

                return res

            return {'status': 400,
                    'message': 'request_id not available. Recover the content of the url by /api/v2/scrape first.'}
        else:

            url_object=db.query(Urls).filter(Urls.request_id == request_id).first()

            res = apis[group][phenomenon](language,url_object.title,url_object.content)

            return res

    else:

        return {'status':500,'message':'Endpoint not available'}


"""




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


    webScraper = News()
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

"""

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080) #10.12.0.3



