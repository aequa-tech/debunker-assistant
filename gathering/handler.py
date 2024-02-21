import requests,random,time
from requests.adapters import HTTPAdapter, Retry
from selenium.webdriver.firefox.options import Options
from selenium import webdriver



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

    def screenscraper(self,path='./geckodriver'):
        '''
        a function that implements a screen scraper with Selenium
        
        PARAMETERS:

        **path**: the path of the driver. 

        OUTPUT:
        
        a Selenium driver
        '''

        options = Options()
        #options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=path,options=options)

        return driver
