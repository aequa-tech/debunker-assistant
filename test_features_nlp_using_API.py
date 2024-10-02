import requests
import json
from requests.auth import HTTPBasicAuth
# domain='http://0.0.0.0:8090'
domain = 'https://api.v1.debunker-assistant.aequa-tech.com'

baseUrl='/internal/v1/'
# Credenziali per l'autenticazione di base
username = "root"
password = "GCsTwJhu?Z#Nua7%+e4zbjtRcFuAeAV"

url='https://www.ilpost.it/2023/12/19/claudio-lotito-senato/?homepagePosition=0'
print(domain + baseUrl +'scrape')
#- DEBUNKER_USERNAME = root
#- DEBUNKER_PASSWORD = GCsTwJhu?Z  # Nua7%+e4zbjtRcFuAeAV
page = requests.post(domain + baseUrl +'scrape', params={'inputUrl': url}, auth=HTTPBasicAuth(username, password))
print(page.text)


request_id=json.loads(page.text)['request_id']

#page=requests.get(domain+'/api/v2/informal_style/use_of_first_and_second_person/'+request_id)

#print(page.text)

#page=requests.get(domain+'/api/v2/informal_style/'+request_id)
#print(page)
#print(page.text)
print(0)
page = requests.post(domain + baseUrl +'article-evaluation', params={'request_id': request_id, 'language':"it"})
print(page)
print(page.text)
print(1)
page=requests.get(domain+baseUrl + 'it/dangerousStyle/irony/'+request_id)
print(page)
print(page.text)
print(2)
page=requests.get(domain+baseUrl +'en/dangerousStyle/'+request_id)
print(page)
print(page.text)