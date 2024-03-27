import time, csv, random
from urllib.parse import urlparse

import pandas as pd
import time
from tqdm import tqdm
# from selenium import webdriver
# from selenium.webdriver import FirefoxOptions
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
import regex as re
from bs4 import BeautifulSoup
import requests
import tldextract

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


class WebCrawler:

    @staticmethod
    def __find_links(a_page, a_domain):
        #print(a_page,a_domain)
        try:
            req = requests.get(a_page, timeout=10,headers=hdr)
            time.sleep(3)
        except Exception as e:
            print(e)
            return [], []
        try:
            soup = BeautifulSoup(req.text, features="html.parser")
            links = soup.find_all('a')

            internal = list()
            external = list()
        except Exception as e:
            print(e)
            return [], []
        for link in links:
            try:
                if link['href'].startswith('/'): #fondamentale per i siti con riferimenti relativi e non assoluti (es. ansa.it)
                    internal.append(a_page.split(':')[0]+'://'+a_domain+link['href'])
                #elif a_domain == tldextract.extract(link['href']).registered_domain:
                elif a_domain == urlparse(link['href']).netloc:
                    internal.append(link['href'])
                else:
                    try:
                        if link['href'].startswith('http'):
                            external.append(re.search('(http|https)://.+?/', link['href']).group())

                    except Exception as e:
                        #print(e)
                        continue
            except Exception as e:
                print(e)
        return internal, external
    @staticmethod
    def retrieveDomains(index_page, domain):
        edges={}
        all_internal = list()
        internal, external = WebCrawler.__find_links(index_page,domain)



        for inter in tqdm(list(internal)[:]):
            time.sleep(1)
            if 'mailto' not in inter:

                try:
                    all_internal.append(inter)

                    new_int, new_ext = WebCrawler.__find_links(inter, domain)
                    for link in new_int:
                        all_internal.append(link)

                    for link in new_ext:
                        external.append(link)

                except Exception as e:
                    print(e)
                    continue

        for url in internal + external+all_internal:
            #target = tldextract.extract(url).registered_domain
            target = urlparse(url).netloc
            edge = domain + ' ' + target
            if edge not in edges: edges[edge] = 0
            edges[edge] += 1

        _edges=[]
        for key, value in edges.items():
            if len(key.split(' '))==2:
                source,target=key.split(' ')
                _edges.append((source,target,value))

        return _edges



if __name__ == "__main__":

    edges=WebCrawler().retrieveDomains('http://ansa.it','ansa.it')
    print(edges)