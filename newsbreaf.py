import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import gathering.handler as hd
import time


handler = hd.SessionHandler()


url = 'https://emm.newsbrief.eu/NewsBrief/searchresults/it/advanced.html?'

params = {'lang':'it',
          'sourceCountry':'it',
          'atLeast':'europa',
          'all':'aborto',
          'dateFrom':'2024-03-13',
          'dateTo':'2024-04-15',
          'queryType':'advanced'


}

for item in params:
    url+=f"&{item}={params[item]}"

print(url)

handler.dynamic_session.get(url)
l = list()
for i in range(500):
    time.sleep(5)
    try:
        page = handler.dynamic_session.page_source

        soup = BeautifulSoup(page)

        for link in soup.find_all('a',attrs={'class':'headline_link'}):
            l.append({'title':link.text,'url':link['href']})

        el = handler.dynamic_session.find_element(By.LINK_TEXT,'>')
        handler.dynamic_session.execute_script("arguments[0].click();",el)
    except Exception as e:
        print(e)
        break

pd.DataFrame(l).drop_duplicates(subset=['title']).to_csv('aborto.csv',index=False)