"""
da usare per controllare il formato di output delle API.
Segnalare gli errori o i dubbi sul formato a mirko

"""
import requests
import json


#domain='0.0.0.0:8090'
domain='api.v1.debunker-assistant.aequa-tech.com'

page=requests.post('https://'+domain+'/internal/v1/internal/scrape',params={'inputUrl':"https://www.ilpost.it/2024/05/15/esercito-israele-rafah-avanzata/?homepagePosition=0" })
print(page.text)
request_id = json.loads(page.text)['result']['request_id']
print(request_id)
language="it"
#page=requests.post(f'http://{domain}/internal/v1/evaluation/{language}/{request_id}',params={ })
#print(page.text)

#page=requests.post(f'http://{domain}/internal/v1/explanation/analysis_id/dangerous',params={ })
#print(page.text)
#page=requests.post(f'http://{domain}/internal/v1/explanation/analysis_id/network',params={ })
#print(page.text)


apis = {
    'informalStyle' : [
         'use_of_first_and_second_person',
         'use_of_personal_style',
         'use_of_intensifier_score',
         'use_of_shorten_form_score',
         'use_of_modals_score',
         'use_of_interrogative_score',
         'use_of_uppercase_words',
         'use_of_repeated_letters',
         'use_of_aggressive_punctuation',
         'use_of_uncommon_punctuation',
         'use_of_emoji',
    ],
    "readability" : [
         'flesch_reading_ease',
    ],
    "clickBait" : [
         'misleading_headline',
    ],
    "affectiveStyle" : [
         'joy',
         'sadness',
         'fear',
         'anger',
         'positiveSentiment',
         'negativeSentiment',
    ],
    "dangerousStyle" : [

        'irony',
        'flame',
        'stereotype',

        ],
    "domainProfile": [

        'backPropagation',

    ],


}

#for group, value in apis.items():
#    for phenomenon in value:
#        print(group, phenomenon)
#        page = requests.get(f'http://{domain}/internal/v1/{language}/{group}/{phenomenon}/{request_id}', params={})
#        print(page.text)

language="en"
for group, value in apis.items():
    page = requests.get(f'http://{domain}/internal/v1/{language}/{group}/{request_id}', params={})
    print(page.text)

page = requests.get(f'http://{domain}/internal/v1/explanations', params={'analysis_id':request_id,'explanation_type' : 'explanationAffective'})
print(page.text)


