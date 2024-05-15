
import requests
import json


domain='0.0.0.0:8090'

page=requests.post('http://'+domain+'/internal/v1/scrape',params={'inputUrl':"https://www.ilpost.it/2024/05/15/esercito-israele-rafah-avanzata/?homepagePosition=0" })
print(page.text)
request_id = json.loads(page.text)['result']['request_id']
print(request_id)
language="it"
page=requests.post(f'http://{domain}/internal/v1/evaluation/{language}/{request_id}',params={ })
print(page.text)

page=requests.post(f'http://{domain}/internal/v1/evaluation/analysis_id/affective',params={ })
print(page.text)
page=requests.post(f'http://{domain}/internal/v1/explanation/analysis_id/dangerous',params={ })
print(page.text)
page=requests.post(f'http://{domain}/internal/v1/explanation/analysis_id/network',params={ })
print(page.text)


