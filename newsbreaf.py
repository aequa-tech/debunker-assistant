import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import gathering.handler as hd
import time


handler = hd.SessionHandler()


url = 'https://emm.newsbrief.eu/NewsBrief/searchresults/it/advanced.html?'

params = {'lang':'it',
          'sourceCountry':'it',
          'atLeast':'pfizer',
          'all':'von,der,leyen',
          'dateFrom':'2024-04-01',
          'dateTo':'2024-04-20',
          'queryType':'advanced'


}

for item in params:
    url+=f"&{item}={params[item]}"

print(url)

handler.dynamic_session.get(url)

for i in range(2):
    time.sleep(5)
    page = handler.dynamic_session.page_source

    soup = BeautifulSoup(page)

    for link in soup.find_all('a',attrs={'class':'headline_link'}):
        print(link.text)

    el = handler.dynamic_session.find_element(By.LINK_TEXT,'>')
    handler.dynamic_session.execute_script("arguments[0].click();",el)