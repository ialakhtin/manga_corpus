import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import os
from common import *

def get_elem_info(ref):
    response = requests.get(ref, headers=headers)
    if response.status_code != 200:
        print(f'elem_alarm {response.status_code} in ref {ref}')
        return None
    soup = BeautifulSoup(response.content, 'lxml')
    content = soup.find(class_=CONTENT_CLASS)
    if content is None:
        print(f'no content in ref {ref}')
        return None
    return content.get_text()


def load_all(max_elem_count=500):
    result = []
    page_id = 0
    while len(result) < max_elem_count:
        page_url = get_page_url(page_id)
        print(f'parsing {page_url}...')
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"page_alarm {response.status_code} on page {page_id}", )
            print(response.content)
            continue
        soup = BeautifulSoup(response.content, 'lxml')
        elems = soup.find_all(class_=ELEMENT_CLASS)
        print(f'found {len(elems)} elements on page {page_id}')
        for elem in elems:
            elem_ref = get_elem_url(elem.get('href'))
            content = get_elem_info(elem_ref)
            if content is None:
                continue
            result.append({'content': content})
            print(f'Parsing: {round(len(result) / max_elem_count * 100, 2)}% completed')
            if len(result) == max_elem_count:
                return result
        page_id += 1
    return result

if __name__ == '__main__':
    elems = load_all()
    out_file = 'texts.json'
    with open(out_file, 'w') as file:
        json.dump(elems, file)
