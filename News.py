import regex as re
import json
import numpy as np
from typing import List
from bs4 import BeautifulSoup
from htmldate import find_date,extractors
from requests import exceptions
from gathering.scraping import Scraper


class News:
    def __init__(self):

        self.scraper = Scraper()

        #specialize htmldate for Italian
        extractors.REGEX_MONTHS = """
        January?|February?|March|A[pv]ril|Ma[iy]|Jun[ei]|Jul[iy]|August|September|O[ck]tober|November|De[csz]ember|
        Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre|
        Gen|Feb|Mar|Apr|Mag|Giu|Lug|Ago|Set|Ott|Nov|Dic|
        Jan|Feb|M[aä]r|Apr|Jun|Jul|Aug|Sep|O[ck]t|Nov|De[cz]|
        Januari|Februari|Maret|Mei|Agustus|
        Jänner|Feber|März|
        janvier|février|mars|juin|juillet|aout|septembre|octobre|novembre|décembre|
        Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık|
        Oca|Şub|Mar|Nis|Haz|Tem|Ağu|Eyl|Eki|Kas|Ara
        """

        extractors.TEXT_MONTHS = {
              # January
              'gennaio': '01',
              "januar": "01",
              "jänner": "01",
              "january": "01",
              "januari": "01",
              "janvier": "01",
              "jan": "01",
              "ocak": "01",
              "oca": "01",
              # February
              'febbraio': '02',
              "februar": "02",
              "feber": "02",
              "february": "02",
              "februari": "02",
              "février": "02",
              "feb": "02",
              "şubat": "02",
              "şub": "02",
              # March
              'marzo': '03',
              "märz": "03",
              "march": "03",
              "maret": "03",
              "mar": "03",
              "mär": "03",
              "mart": "03",
              "mars": "03",
              # April
              'aprile': '04',
              "april": "04",
              "apr": "04",
              "avril": "04",
              "nisan": "04",
              "nis": "04",
              # May
              'Maggio': '05',
              "mai": "05",
              "may": "05",
              "mei": "05",
              "mayıs": "05",
              # June
              'giugno': '06',
              "juni": "06",
              "june": "06",
              "juin": "06",
              "jun": "06",
              "haziran": "06",
              "haz": "06",
              # July
              'luglio': '07',
              "juli": "07",
              "july": "07",
              "juillet": "07",
              "jul": "07",
              "temmuz": "07",
              "tem": "07",
              # August
              'agosto': '08',
              "august": "08",
              "agustus": "08",
              "aug": "08",
              "ağustos": "08",
              "ağu": "08",
              "aout": "08",
              # "août": "08",
              # September
              'settembre': '09',
              "september": "09",
              "septembre": "09",
              "sep": "09",
              "eylül": "09",
              "eyl": "09",
              # October
              'ottobre': '10',
              "oktober": "10",
              "october": "10",
              "octobre": "10",
              "oct": "10",
              "okt": "10",
              "ekim": "10",
              "eki": "10",
              # November
              'novembre': '11',
              "november": "11",
              "nov": "11",
              "kasım": "11",
              "kas": "11",
              "novembre": "11",
              # December
              'dicembre': '12',
              "dezember": "12",
              "december": "12",
              "desember": "12",
              "décembre": "12",
              "dec": "12",
              "dez": "12",
              "aralık": "12",
              "ara": "12",}

    def get_news_from_url(self, url):

        status, text = self.scraper.scrape_page(url)

        if status == 200:
            title,article_text,date = self._get_news_info(text)
            urls = self._get_URLs_in_news(url, text)
            return json.dumps({'status':200, 'message':'the request was successful', 'result' : {'title':title, 'content': article_text, 'date':date, 'urls':urls} })
        else:
            return json.dumps({'status': status, 'message': text })

    def _get_news_info(self, text):

        soup = BeautifulSoup(text, features="html.parser")

        title = ''
        hs = soup.find_all(["h1", "h2", "h3", 'h4'],
                           class_={lambda x: "post-title" in x.lower() or "entry-title" in x.lower()})
        h_index = 5
        for h in hs:
            cur_h_index = int(h.name[-1])
            if title == '' and cur_h_index < h_index:
                title = re.sub(' +', ' ', h.text.strip().replace("/n", ''))
                h_index = cur_h_index

        if title == '':
            title = soup.title.text

        article_text = ''
        articles = soup.find_all('article')
        if len(articles) == 0:
            container,_class_ = self._compile_args()
            articles = soup.find_all(container, attrs={'class':_class_})

        if len(articles)>0:
            #ids = [x.text for x in articles]
            #max_id = np.argmax(ids)
            #article_text = articles[max_id].text
            for article in articles:
                ps = article.findAll('p')
                for p in ps:
                    article_text += '\n' + ''.join(p.findAll(string=True))

        if len(article_text) == 0:
            ps = soup.findAll('p')
            for p in ps:
                article_text += '\n' + ''.join(p.findAll(string=True))



        article_text=article_text.replace("\n"," ")
        date = find_date(text)

        return title,article_text,date

    def _get_URLs_in_news(self, domain, text):
        urls=[]
        setUrls=()

        soup = BeautifulSoup(text, features="html.parser")

        hrefs = soup.find_all('a')
        for href in hrefs:
            if not href.has_attr('href'):
                continue
            if not href['href'].startswith("/") and not href['href'].startswith("http"):
                continue
            has_child=""
            for child in href.findChildren():
                has_child+=" "+child.name

            if href['href'].startswith("/"):
                url = domain + href['href']
            else:
                url=href['href']
            url = url.split("://")[-1].split("www.")[-1].split('?')[0].split('#')[0]
            urls.append({
                "url" : url,
                "text": re.sub(" +"," ",href.text.strip()),
                "tags": has_child.strip(),
                "flag": self._check_domain(href['href'])
            })
        return urls

    def _check_domain(self, link: str, flag='both') -> int:

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

        external_block = ['amazon', 'amzn', 'twitter', 'facebook', 'instagram', 'cookies', 't.co', 't.me', 'tiktok',
                          'pinterest', 'youtube', 'whatsapp', 'telegram', 'apple','adobe']

        internal_block = ['subscribe\.', 'abbonati\.', 'privacy', 'cooki(e|es)', 'edicola\.', 'shop\.', 'login',
                          'log-in', 'signin', 'sign-in', 'wp-', 'signup', 'sign-up', 'paywall']

        if flag == 'external':
            flag = 1 if re.search('|'.join(external_block), link) else 0

        elif flag == 'internal':
            flag = 1 if re.search('|'.join(internal_block), link) else 0

        else:
            flag = 1 if re.search('|'.join(external_block + internal_block), link) else 0

        return flag
    
    def _compile_args(self,container:List=['div','section'],_class_:List=['post','entry','artic']):

        container = re.compile('|'.join(container))
        _class_ = re.compile('|'.join(_class_))

        return container,_class_


if __name__ == "__main__":
    webScraper=News()

    result=webScraper.get_news_from_url('https://www.ilfattoquotidiano.it/in-edicola/articoli/2024/03/28/crosetto-vendute-armi-a-kiev-per-417-milioni-camere-ignare/7494186/')
    print(result)
    result=webScraper.get_news_from_url('https://www.ilfattoquotidiano.it/?refresh_ce')
    print(result)
    result=webScraper.get_news_from_url('https://www.ilfattoquotidiano.it/in-edicola/articoli/2024/03/28/crosetto-vendute-armi-a-kiev-per-417-milioni-camere-ignare/7494186/')
    print(result)
