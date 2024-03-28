from functools import lru_cache

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
from gathering.handler import SessionHandler


class Scraper:
    def __init__(self):
        self.session_handler = SessionHandler()



    def _build_http_url(self, url):
        if len(url.split('?url=')) > 1:
            url = url.split('?url=')[1]
        if len(url.split('?u=')) > 1:
            url = url.split('?u=')[1]

        url = url.split("://")[-1]

        url = 'http://{}'.format(url)

        return url

    def _build_https_url(self, url):
        if len(url.split('?url=')) > 1:
            url = url.split('?url=')[1]
        if len(url.split('?u=')) > 1:
            url = url.split('?u=')[1]

        url = url.split("://")[-1]

        url = 'https://{}'.format(url)

        return url

    def _test_content(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        resp = self.session_handler.static_session.request('HEAD', self._build_http_url( url), headers=headers)
        print(resp)
        if resp.status_code == 200:
            if 'text/html' not in resp.headers['Content-Type']:
                return 400, 'the API exclusively satisfies text/html Content-Types. The current Content-Type is '
            else:
                return 200, self._build_http_url(url)
        elif resp.status_code == 403:
            print(403)
            print(url)
            print( self._build_https_url(url))
            resp = self.session_handler.static_session.request('HEAD', self._build_https_url(url), headers=headers)
            if resp.status_code == 200:
                if 'text/html' not in resp.headers['Content-Type']:
                    return 400, 'the API exclusively satisfies text/html Content-Types. The current Content-Type is '
                else:
                    print(resp.text)
                    return 200, self._build_https_url(url)
            else:
                print('qui')
                return 400, 'the requested url is not available'

    def _scrapeDynamicPage(self, url):

        url = self._build_url(url)

        html = self.session_handler.dynamic_session.get(url)
        self.session_handler.execute_script("window.scrollTo(0, document.body.scrollHeight);",html)
        page = self.session_handler.page_source

        return page



    @lru_cache(maxsize=32)
    def _scrapeStaticPage(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = self.session_handler.static_session.get(url,headers=headers)

        return page.status_code,page.text

    @lru_cache(maxsize=32)
    def scrape_page(self, url):

        status, url = self._test_content(url)
        if status != 200:
            return status, url

        #try:
        status, page = self._scrapeStaticPage(url)
        if status == 403:
            status, page = self._scrapeDynamicPage(url)

        return status,page
        #except Exception as e:
        #    return 500, str(e)



