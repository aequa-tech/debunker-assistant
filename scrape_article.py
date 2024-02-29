import pandas as pd
from tqdm import tqdm
import gathering.scraper as gat
import gathering.handler as hd
import data.connector as cn
from sqlalchemy import text
import time


connector = cn.Connector()
engine = connector.engine_postgres(user='debunker',passw='A283hnd(902!)?]',host='db.aequa-tech.com:54321',db='DA')

hand = hd.SessionHandler()

url = hand.urllib()
scrap = gat.NewsScraper()

tab = connector.read(engine,'select distinct url,domain from seed where flag = 0')

tab = [row for row in tab if not row[0].startswith('http')]
print(tab)
tab = [('ilpost.it/2024/02/29/sgomberi-case-occupate-caivano','ilpost.it')]
for row in tab:
    link = scrap.build_url(row[0])
    d = dict()
    d['url'] = row[0]

    try:
        pg = url.get(link)
    except Exception as e:print(e)
    
    try:
        if pg.status_code == 403:
            screen = hand.screenscraper()
            pg = scrap.get_page(screen,link)
    except Exception as e: print(e)
    
    try:
        title, page = scrap.parse_page(pg) if type(pg) is str else scrap.parse_page(pg.text)
        d['title'] = title
        
        claims = scrap.find_claims(row[0],page)
        claims = list(set(claims))
        d['page'] = scrap.find_page(page)

        claims = [{'url':x[0],"target":x[1],'claim':x[2]} for x in claims]
        with engine.connect() as conn:
            conn.execute(text(f'INSERT INTO pages ("url","title","page") VALUES(:url,:title,:page)'),[d])
            conn.execute(text(f'INSERT INTO claims ("url","target","claim") VALUES(:url,:target,:claim)'),claims)
            
            conn.commit()
        
        time.sleep(1)
    
    except: continue

