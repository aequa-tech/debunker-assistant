import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, Urls, get_db, Requests
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import numpy
import hashlib
import json
from datetime import datetime, time,timedelta
from urllib.parse import urlparse

from News import News

from features.nlp.affective import Sentiment, Emotion
from features.nlp.danger    import Irony, Flame, Stereotype
from features.nlp.scores    import InformalStyle, ClickBait, Readability

import yaml

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

with open('payload.yaml') as f:
    result = yaml.load(f, Loader=yaml.FullLoader)

@app.post(basePath+"{language}/{request_id}")
async def evaluation(request_id : str, language: str = 'it'):
    result['evaluation']

@app.post(basePath+"{analysis_id}/{explanation_type}")
async def explanation(analysis_id : str, explanation_type : str):
    if explanation_type == 'affective':
        result['explanation']['explanationAffective']
    elif explanation_type == 'dangerous':
        result['explanation']['explanationDangerous']
    elif explanation_type == 'network':
        result['explanation']['explanationNetwork']


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)