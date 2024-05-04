import requests
import json

domain='http://0.0.0.0:8090'
baseUrl='/internal/v1/'

url='https://www.ilpost.it/2023/12/19/claudio-lotito-senato/?homepagePosition=0'

page = requests.post(domain + baseUrl +'scrape', params={'inputUrl': url})
print(page.text)


request_id=json.loads(page.text)['result']['request_id']

#page=requests.get(domain+'/api/v2/informal_style/use_of_first_and_second_person/'+request_id)

#print(page.text)

#page=requests.get(domain+'/api/v2/informal_style/'+request_id)
#print(page)
#print(page.text)
print(0)
page = requests.post(domain + baseUrl +'article-evaluation', params={'request_id': request_id})
print(page)
print(page.text)

exit(0)


print(1)
page=requests.get(domain+'/api/v2/dangerous_speech_acts/irony/'+request_id)
print(page)
print(page.text)
print(2)
page=requests.get(domain+'/api/v2/dangerous_speech_acts/'+request_id)
print(page)
print(page.text)