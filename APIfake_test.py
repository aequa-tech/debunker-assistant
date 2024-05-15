
import requests


domain='test.aequa-tech.com'

page=requests.post('https://'+domain+'/internal/v1/evaluation/{language}/{request_id}',params={ })
print(page.text)

page=requests.post('https://'+domain+'/internal/v1/explanation/analysis_id/affective',params={ })
print(page.text)
page=requests.post('https://'+domain+'/internal/v1/explanation/analysis_id/dangerous',params={ })
print(page.text)
page=requests.post('https://'+domain+'/internal/v1/explanation/analysis_id/network',params={ })
print(page.text)


