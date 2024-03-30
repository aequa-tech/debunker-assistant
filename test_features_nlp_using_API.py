import requests
import json

domain='http://0.0.0.0:8090'


url='https://www.ilpost.it/2023/12/19/claudio-lotito-senato/?homepagePosition=0'

page = requests.post(domain + '/api/v2/scrape', params={'url': url})
print(page.text)


request_id=json.loads(page.text)['result']['request_id']


#page=requests.get(domain+'/api/v2/informal_style/use_of_first_and_second_person/'+request_id)

#print(page.text)

#page=requests.get(domain+'/api/v2/informal_style/'+request_id)
#print(page)
#print(page.text)
print(0)
page=requests.get(domain+'/api/v2/sentiment/positive/'+request_id)
print(page)
print(page.text)

print(1)
page=requests.get(domain+'/api/v2/dangerous_speech_acts/irony/'+request_id)
print(page)
print(page.text)
print(2)
page=requests.get(domain+'/api/v2/dangerous_speech_acts/'+request_id)
print(page)
print(page.text)