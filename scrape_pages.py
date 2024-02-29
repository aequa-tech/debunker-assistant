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
df = pd.read_csv('/home/marco/seeds.csv')

for i,row in tqdm(df[304:].iterrows()):
    link = scrap.build_url(row[0])
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
        
        internal,external = scrap.find_links(row[0],page)
        internal = list(set(internal))
        external = list(set(external))
        ext_flag = [scrap.check_domain(x) for x in external]
        int_flag = [scrap.check_domain(x) for x in internal]
        internal = list(zip(internal,int_flag))
        
        external = list(zip(external,ext_flag))
        internal = [{'url':x[0],'flag':x[1],'domain':row[0]} for x in internal]
        external = [{'url':x[0],'flag':x[1],'domain':row[0]} for x in external]
        
        links = internal+external
        
        
        with engine.connect() as conn:
            conn.execute(text(f'INSERT INTO urls ("url","flag","domain") VALUES(:url,:flag,:domain)'),links)
            conn.commit()
        
        time.sleep(1)


    
    except Exception as e: print(e)
