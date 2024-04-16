import time,csv,random,json,requests
from typing import List,Tuple
import logging as log
import pandas as pd
from tqdm import tqdm
import numpy as np
import regex as re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import psycopg2
from requests.adapters import HTTPAdapter, Retry

log.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=log.INFO,
    datefmt='%d/%m/%Y %H:%M:%S'
)


class ManageDB:
    def __init__(self):
        pass

    def connect(self,dbname,user,password,host='localhost',port=5432):

        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,  # Indirizzo del server PostgreSQL
            port=port        # Porta di default di PostgreSQL
            
        )
        cursor = connection.cursor()

        return connection,cursor
    
    def read(self,query,cursor,param=None):
        
        if param is None:

            cursor.execute(query)
        else:
            cursor.execute(query.format(param))
        read_output = cursor.fetchall()

        return read_output
    
    def update(self,query,data,cursor,connection):

        try:
            cursor.execute("BEGIN;")
            cursor.execute(query,(data[0],data[1]))
            connection.commit
        except Exception as e: log.info(f'error updating beacause {e}')

    def write_many(self,query,data:List[List],cursor,connection):
        cursor.execute("BEGIN;")
        
        try:
            cursor.executemany(query,data)
            connection.commit()
            log.info('writing operation was successful')
            
        except Exception as e:
            log.info(f'error writing because {e}')

    def write_one(self,query,data:Tuple,cursor,connection):
        cursor.execute("BEGIN;")
        
        try:
            cursor.executemany(query,data)
            connection.commit()
            log.info('writing operation was successful')
            
        except:
            log.info('error writing')


