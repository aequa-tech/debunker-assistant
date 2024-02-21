import requests,random,time
from requests.adapters import HTTPAdapter, Retry
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import regex as re
import numpy as np
from nltk.tokenize import sent_tokenize

class SessionHandler:
    def __init__(self):
        pass
    
    def urllib(self,retries=3,backoff=1):
        '''
        a function that implements a scraper with requests
        
        PARAMETERS
        **retries**: the number of connection attempts after a fail. By default it is set to 3
        **backoff**: it sets the backoff_factor, which impacts on the waiting time between retries. By default it is set to 1

        OUTPUT:

        a requests session
        '''

        session = requests.Session()
        retries = Retry(total=retries, backoff_factor=backoff, status_forcelist=[ 502, 503, 504 ])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        
        return session

    def screenscraper(self,path='.'):
        '''
        a function that implements a screen scraper with Selenium
        
        PARAMETERS:

        **path**: the path of the driver. 

        OUTPUT:
        
        a Selenium driver
        '''

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=path,options=options)

        return driver


class NewsScraper:
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
        url = 'http://{}'.format(domain)

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
        time.sleep(random.random(1,5))
        html.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page = html.page_source

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
        links = [x['href'] for x in page.find_all('a')]
        internal_a = [x.split('?')[0].split('//')[-1] for x in links if domain in links]
        internal_b = ['{}{}'.format(x,domain) for x in links if x.startswith('/')]

        internal = list(set(internal_a+internal_b))
        
        external = list()
        for link in links:
            try:
                if domain not in link and link.startswith('http'):
                    external.append(re.search('(http|https)://.+?/',link))
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
    

    def check_domain(self,link,flag='both'):

        
        external_block = ['amazon','amzn','twitter','facebook','instagram','cookies','t.co','t.me','tiktok','pinterest','youtube']

        internal_block = ['subscribe\.','abbonati\.','privacy','cooki(e|es)','edicola\.','shop\.','login','log-in','signin','sign-in','wp-','signup','sign-up']

        if flag == 'external':
            flag = 1 if re.search('|'.join(external_block,link)) else 0
        
        elif flag == 'internal':
            flag = 1 if re.search('|'.join(internal_block,link)) else 0
        
        else:
            flag = 1 if re.search('|'.join(external_block+internal_block,link)) else 0
        
        return flag







