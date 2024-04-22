import requests,random,time
from requests.adapters import HTTPAdapter, Retry
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import regex as re
import numpy as np
from typing import List



class NewsCrawling:
    def __init__(self):
        pass


    def build_url(self,domain):

        '''
        The function builds the url, given a domain

        PARAMETERS

        **domain**: the domain that is used as a base to build the url

        OUTPUT:

        the url
        '''
        url = 'http://{}'.format(domain) #da capire

        return url
    

    def get_page(self,driver,url):

        '''The function takes as input an url and return its raw html page
        
        PARAMETERS
        
        **driver**: a Selenium driver
        **url**: the url that you want to scrape
        
        OUTPUT:
        
        a document with the gathered page
        '''

        html = driver.get(url)
        time.sleep(random.randint(1,5))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);",html)
        page = driver.page_source

        return page            

    
    def parse_page(self,page):

        '''
        The function takes as an input a page, parses it and returns it and page's title

        PARAMETERS

        **page**: a string containing an html page

        OUTPUT

        the page's title
        the parsed page
        '''

        parsed_page = BeautifulSoup(page,features='html.parser')

        title = parsed_page.title.text

        return title,parsed_page
    
    def find_links(self,domain,page):

        '''
        this function retrieves all links in a page and divides them in internal and external

        PARAMETERS

        **domain**: a domain without any 'http' or 'www' at the beginning
        **page**: a parsed page with BeutifulSoup. If you want, you can use the function 'parse_page()' to do that before calling this function

        OUTPUT

        **internal**: a list of internal links
        **external**: a list of external links
        '''
        
        domain = domain[:-1] if domain.endswith('/') else domain
        links = list()
        for item in page.find_all('a'):
            try:
                links.append(item['href'])
            except: continue
        #links = [x['href'] for x in page.find_all('a') if 'href' in x]
        
        internal_a = [x.split('?')[0].split('//')[-1] for x in links if domain in links]
        internal_b = ['{}{}'.format(domain,x) for x in links if x.startswith('/')]

        internal = list(set(internal_a+internal_b))
        
        external = list()
        for link in links:
            try:
                if domain not in link and link.startswith('http'):
                    external.append(re.search('(http|https)://.+?/',link).group())
            except: continue
        
        return internal,external
    
    def find_claims(self,domain,page):

        ''' this function retrieves all claims in form of triples of the type (domain,url,text)
        
        PARAMETERS
        
        **domain**: a domain without any 'http' or 'www' at the beginning
        **page**: a parsed page with BeutifulSoup. If you want, you can use the function 'parse_page()' to do that before calling this function

        OUTPUT

        a list of triples of the type (domain,url,text)
'''

        claims = list()
        divs = page.find_all('div')
        
        
        if len(divs)>0:
            max_length = np.argmax([len(x.text) for x in divs])
            pars = divs[max_length].find_all('p')
            
        else:
            pars = page.find_all('p')
        
        for par in pars:
            claims.extend([(domain,x['href'],x.text) for x in par.find_all('a')])
        
        


        return claims
    
    def find_page(self,page):
        
        ''' this function retrieves a page
        
        PARAMETERS
        
        **domain**: a domain without any 'http' or 'www' at the beginning
        **page**: a parsed page with BeutifulSoup. If you want, you can use the function 'parse_page()' to do that before calling this function

        OUTPUT

        a list of triples of the type (domain,url,text)
'''


        claims = list()
        divs = page.find_all('div')
        if len(divs)>0:
            max_length = np.argmax([len(x.text) for x in divs])
            pars = divs[max_length].find_all('p')
        else:
            pars = page.find_all('p')
        
        text = ''

        for p in pars:
            text+='{} '.format(p.text)
        
        return text
        

    def check_domain(self,link:str,flag='both') -> int:

        '''
        This function add a flag to a page if the url match some strings that may correlate with non-relevant contents (eg: privacy policy page)

        PARAMETERS:

        **link**: the link to be checked
        **flag**: the type of check. 'internal' only checks for internal non-relevant pages (eg: subscribe page); `external' for external ones 
        (eg: links to whatsapp). 'both' checks for both

        OUTPUT:
        value 1 if there are some flags, 1 if there aren't
        '''

        assert type(link) is str, "wrong type for link"

        external_block = ['amazon','amzn','twitter','facebook','instagram','cookies','t\.co','t\.me','tiktok','pinterest','youtube','whatsapp','telegram','apple','m\.me','spotify','goo\.gl','bit\.ly','linkedin','google','shopify','^wordpress\.org','wikipedia\.org']

        internal_block = ['subscribe\.','abbonati\.','privacy','cooki(e|es)','edicola\.','shop\.','login','log-in','signin','sign-in','wp-','signup','sign-up','paywall','\.png$','\.jpg$','\.pdf$']

        if flag == 'external':
            flag = 1 if re.search('|'.join(external_block),link) else 0
        
        elif flag == 'internal':
            flag = 1 if re.search('|'.join(internal_block),link) else 0
        
        else:
            flag = 1 if re.search('|'.join(external_block+internal_block),link) else 0
        
        return flag

class FacebookScraper:
    def __init__(self):
        pass

    def login(self,driver,user,passw):
        

        driver.get("http://www.facebook.com")
        time.sleep(3)

        accept = driver.find_element(By.XPATH,"//button[@title='Decline optional cookies']")
        driver.execute_script("arguments[0].click();" ,accept)
        time.sleep(2)

        username = driver.find_element(By.ID,"email")
        password = driver.find_element(By.ID,"pass")

        submit   = driver.find_element(By.XPATH,"//button[text()='Log In']")
        
        username.send_keys(user)
        password.send_keys(passw)

        time.sleep(2)
        driver.execute_script("arguments[0].click();" ,submit)

        return driver











