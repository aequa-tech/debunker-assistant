import requests,csv
import pandas as pd
import argparse,json
from bs4 import BeautifulSoup
from tqdm import tqdm
parser = argparse.ArgumentParser()

parser.add_argument('-f','--filename')


args = parser.parse_args()

df = pd.read_csv(args.filename)





wikidata_ids = ''
wikipedia_ids = ''





def find_wiki_titles(a_list):
	wikidata = 'https://www.wikidata.org/w/api.php'
	wd_params =  {'format':'json','action':'wbgetentities','ids':'{}'.format('|'.join(a_list)),'props':'sitelinks','languages':'en'}
	req = requests.get(wikidata,params=wd_params)
	titles = list()
	for item in req.json()['entities']:
		try:
			titles.append((item,req.json()['entities'][item]['sitelinks']['enwiki']['title']))
		except: continue
	
	return titles

def find_claims(a_list):
	wikidata = 'https://www.wikidata.org/w/api.php'
	wd_params =  {'format':'json','action':'wbgetentities','ids':'{}'.format('|'.join(a_list)),'props':'claims','languages':'en'}
	req = requests.get(wikidata,params=wd_params)
	titles = list()
	for item in req.json()['entities']:
		try:
			titles.append((item,req.json()['entities'][item]['claims']['P17'][0]['mainsnak']['datavalue']['value']['id']))
		except Exception as e:continue
	
	return titles

def find_labels(a_list):
	wikidata = 'https://www.wikidata.org/w/api.php'
	wd_params =  {'format':'json','action':'wbgetentities','ids':'{}'.format('|'.join(a_list)),'props':'labels','languages':'en'}
	req = requests.get(wikidata,params=wd_params)
	titles = list()
	for item in req.json()['entities']:
		try:
			titles.append((item,req.json()['entities'][item]['labels']['en']['value']))
		except Exception as e:print(e)
	
	return titles

	
	

def find_wp_pages(a_string):
	wikipedia = 'https://en.wikipedia.org/w/api.php'
	
	wiki_params ={'action':'parse','page':'{}'.format(a_string),'format':'json'}

	req = requests.get(wikipedia,params=wiki_params)
	
	try:
		page = req.json()['parse']['text']
		return page
	except: 
		return None

def find_multiple_wp_pages(a_list):
	wikipedia = 'https://en.wikipedia.org/w/api.php'
	
	names = '|'.join([x[1] for x in a_list])
	mapping = {x[1]:x[0] for x in a_list}
	wiki_params = {'action':'query','prop':'revisions','titles':names,'format':'json','rvprop':'content'}
	
	req = requests.get(wikipedia,params=wiki_params)
	res = list()

	for item in req.json()['query']['pages']:
		
		try:
			d = dict()
			d['title'] = req.json()['query']['pages'][item]['title']
			d['wd_id'] = mapping[d['title']]
			d['txt'] = req.json()['query']['pages'][item]['revisions'][0]['*']
			res.append(d)
		except Exception as e:print(e)
	return res
	
titles = df.P19.to_list()
chunks = [titles[x:x+50] for x in range(0, len(titles), 50)]

fo = open('nyt_rels/nyt_cob.csv',mode='w')
writer = csv.DictWriter(fo,fieldnames=['P19','P17'])
writer.writeheader()
l = list()
for i,chunk in tqdm(enumerate(chunks),total=len(chunks)):
	try:
		w_titles = find_claims(chunk)
		for item in w_titles:
			try:
				writer.writerow({'P19':item[0],'P17':item[1]})
			except:continue
		'''w_pages = find_multiple_wp_pages(w_titles)
		with open('/media/marco/BE24B62524B5E097/wiki_biographies/{}.json'.format(i), mode='w') as f:
			json.dump(w_pages,f)'''
		
	except Exception as e:print(e)
'''
titles = df.to_numpy()

for title in tqdm(titles[133000:]):
	try:
		w_page = find_wp_pages(title[1])
		with open('monte_carlo/wpages/{}.txt'.format(title[0]),mode='w') as f:
			f.write(w_page['*'])
	except Exception as e:print(e)
		
'''
