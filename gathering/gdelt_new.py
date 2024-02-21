import time,csv,random,json,requests
import pandas as pd
from tqdm import tqdm
import numpy as np
import regex as re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import psycopg2
from requests.adapters import HTTPAdapter, Retry


conn = psycopg2.connect(
	dbname='mydb',
	user='postgres',
	password='H4n4m1ch1!',
	host='localhost',  # Indirizzo del server PostgreSQL
	port='5432'        # Porta di default di PostgreSQL
)

cur = conn.cursor()

cur.execute("SELECT * FROM domains where scraped=0")


domains = cur.fetchall()


def do_request():
	s = requests.Session()
	retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
	s.mount('http://', HTTPAdapter(max_retries=retries))

	return s

def find_links(a_page,a_domain,a_list):
	soup = BeautifulSoup(a_page,features='html.parser')
	links = soup.find_all('a')
	internal = set()
	external = list()
	for link in links:
		try:
			if a_domain in link['href']:
				
				internal.add(link['href'].split('?')[0])
				
			elif link['href'].startswith('http') and re.search('|'.join(a_list),link['href']) is None:
					external.append(re.search('(http|https)://.+?/',link['href']).group())
		except:
			continue
	return internal,external

def find_claims(a_page,a_url):
	claims = list()
	
	soup = BeautifulSoup(a_page,features='html.parser')
	divs = soup.find_all('div')
	title = soup.title.text
	if len(divs)>0:
		max_length = np.argmax([len(x.text) for x in divs])
	
		pars = divs[max_length].find_all('p')
	else:
		pars = soup.find_all('p')
	for par in pars:
		if par.find('a'):
			urls = {x.text:x['href'] for x in par.find_all('a')}
			for el in urls:
				for p in sent_tokenize(par.text):
					
					if re.search(el,p):
						d = (a_url,urls[el],re.search(el,p).group(),p)
						claims.append(d)
	
	return claims,pars,title
				
	
	

req = do_request()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

block_domains = ['amazon','amzn','twitter','facebook','instagram','cookies','t.co','t.me','tiktok','pinterest','youtube']

for row in domains:
	dom = row[0].split('//')[-1]
	
	
	page = req.get(row[0],headers=headers)

	all_internal = set()
	
	internal,external = find_links(page.text,dom,block_domains)
	

	all_claims = list()
	all_urls = list()
	all_pars = list()

	for inter in tqdm(internal):
		try:
			
			all_internal.add(inter)
			page = requests.get(inter)
			time.sleep(1)
			claims,pars,title = find_claims(page.text,inter)
			pars = [(inter,i,par.text) for i,par in enumerate(pars)]
			all_pars.extend(pars)
			for claim in claims:
				all_claims.append(claim)

			ext_url = len([x for x in claims if dom not in x[1]])
			
			int_url = len([x for x in claims if dom in x[1]])
			all_urls.append((inter,title,ext_url,int_url,row[0]))

			new_int,new_ext = find_links(page.text,dom,block_domains)
			
			for link in new_int: all_internal.add(link)
			for link in new_ext: external.append(link)
		except Exception as e: print(e)
	try:
		df = pd.DataFrame(all_claims,columns=['url','ext_link','link_text','sentence'])
		df = df.drop_duplicates(subset=['ext_link','link_text','sentence'])
		all_claims = df.to_numpy()
		external = pd.DataFrame(external,columns=['target'])
		external['domain'] = row[0]
		external = external.value_counts().reset_index()
		external.columns = ['target','domain','n_link']
		ext_domains = external
		ext_domains['scraped'] = 0
		ext_domains = ext_domains[['target','scraped']].to_numpy()
		external = external[['domain','target','n_link']].to_numpy()

		cur.execute("BEGIN;")
		cur.executemany("INSERT INTO claims (url,ext_link,link_text,sentence) VALUES (%s,%s,%s,%s)",all_claims)
		cur.executemany("INSERT INTO pars (url,_id,paragraph) VALUES (%s,%s,%s)",all_pars)
		cur.executemany("INSERT INTO news (url,title,ext_link,int_link,domain) VALUES (%s,%s,%s,%s,%s)",all_urls)
		cur.executemany("INSERT INTO ext_link (domain,target,n_link) VALUES (%s,%s,%s)",external)
		cur.execute("UPDATE domains SET scraped = %s WHERE domain = %s", (1,row[0]))
		cur.executemany("INSERT INTO domains (domain,scraped) values (%s,%s) ON CONFLICT (domain) DO UPDATE SET domain=domains.domain",ext_domains)
		conn.commit()
	except Exception as e:print(e)


driver.close()
