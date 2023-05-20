headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 '
                   'Firefox/14.0.1'),
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':
    'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':
    'gzip, deflate',
    'Connection':
    'keep-alive',
    'DNT':
    '1'
}

ELEMENT_CLASS = 'more-link'
CONTENT_CLASS = 'description manga-description'
URL_PREFIX = 'https://readmanga.live'

def get_page_url(page_id):
    return URL_PREFIX+f'/review/list?offset={page_id*20}'

def get_elem_url(url):
    return URL_PREFIX + url

TEXTS_FILE = 'texts.json'
SENTENCES_FILE = 'sentences.json'