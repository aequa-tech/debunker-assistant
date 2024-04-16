import News
import psycopg2,yaml, argparse,json
import logging as log
import pandas as pd
from gathering import debunker_db

parser = argparse.ArgumentParser()

parser.add_argument('-c','--config')
args = parser.parse_args()


with open(args.config) as f:
    vars = yaml.load(f, Loader=yaml.FullLoader)

mydb = debunker_db.ManageDB()

connection,cursor = mydb.connect(vars['db']['dbname_it'],vars['db']['user'],vars['db']['password'])

cursor.execute(vars['create']['seeds'])
cursor.execute(vars['create']['claims'])
cursor.execute(vars['create']['network'])
connection.commit()


df = pd.read_csv('seeds.csv')
df['network'] = 0
df['scraped'] = 0
seeds = [[row[0],row[1],row[-2],row[-1]] for row in df.to_numpy()]
print(seeds)
mydb.write_many(vars['insert']['seeds'],seeds,cursor,connection)
d = {1:'secondary',2:'tertiary'}

webScraper = News.News()
for i in range(3):
    seeds = mydb.read(vars['read']['seeds'],cursor,(i,0))
    
    for seed in list(seeds):
        log.info(f'we are scraping {seed}')
        try:
            out = webScraper.get_news_from_url(seed[0])
            res = json.loads(out)
            network = {(x['url'].split('/')[0],d[i+1],i+1,0) for x in res['result']['urls'] if x['flag']!=1}
            print(network)
            targets = {(seed[0],x['url'].split('/')[0]) for x in res['result']['urls'] if seed[0] not in x['url']}
            claims = {(seed[0],x['url'],x['text'],x['flag']) for x in res['result']['urls']}
            mydb.write_many(vars['insert']['seeds'],network,cursor,connection)
            mydb.write_many(vars['insert']['network'],targets,cursor,connection)
            mydb.write_many(vars['insert']['claims'],claims,cursor,connection)
            mydb.update(vars['update']['seeds'],(1,seed[0]),cursor,connection)
        except Exception as e: 
            mydb.update(vars['update']['seeds'],(-1,seed[0]),cursor,connection)
            log.info(e)


