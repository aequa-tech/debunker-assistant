import requests,re,json
from bs4 import BeautifulSoup
from htmldate import find_date,extractors
from requests import exceptions



class WebScraper:
    def __init__(self):
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

    def scrape(self,url):

        try:

            if len(url.split('?url=')) > 1:
                url = url.split('?url=')[1]
            if len(url.split('?u=')) > 1:
                url = url.split('?u=')[1]

            resp = requests.request('HEAD', url,headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

            if resp.status_code == 200:
                if 'text/html' not in resp.headers['Content-Type']:
                    return json.dumps({'status': 400, 'message': 'the API exclusively satisfies text/html Content-Types. The current Content-Type is '+resp.headers['Content-Type']})
            else:
                return json.dumps({'status': 400, 'message': 'the requested url is not available'})

            page = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            text = page.text
            if page.status_code == 200:
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
                    articles = soup.find_all('div', class_={
                        lambda x: "post" in x.lower() or "entry" in x.lower() or "artic" in x.lower()})

                for article in articles:
                    ps = article.findAll('p')
                    for p in ps:
                        article_text += '\n' + ''.join(p.findAll(string=True))

                if len(article_text) == 0:
                    ps = soup.findAll('p')
                    for p in ps:
                        article_text += '\n' + ''.join(p.findAll(string=True))

                date = find_date(text)
                return json.dumps({'status':200, 'message':'the request was successful', 'result' : {'title':title, 'content': article_text, 'date':date} })
            else:
                return json.dumps({'status':400, 'message':'the requested url is not available'})

        except exceptions.RequestException:
            return json.dumps({'status': 400, 'message': 'the requested url is not available'})
        except Exception:
            return json.dumps({'status':500,'message':'something goes wrong'})

if __name__ == "__main__":
    webScraper=WebScraper()

    result=webScraper.scrape('https://www.pianetablunews.it/2023/04/28/si-rifiuta-di-andare-in-una-casa-di-riposo-senza-i-suoi-gatti-e-la-struttura-inaugura-un-piccolo-rifugio-per-accoglierli/')
    print(result)
