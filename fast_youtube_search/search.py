import requests
import sys
import json
from functools import reduce
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger_chardet = logging.getLogger('chardet.charsetprober')
logger_chardet.setLevel(logging.INFO)

def extract_data( el ):
    if el.a and el.div and ('yt-lockup-video' in el.div['class']) and el.h3 and el.h3.a:
        video_id = el.a['href'].split('=')[1]
        return {
            'name': el.h3.a.text,
            'id': video_id,
            'img': 'https://i.ytimg.com/vi/' + video_id + '/hqdefault.jpg'
        }

def get_html( transformed_query ):
    BASE_URL = 'https://www.youtube.com/results?search_query='
    URL = BASE_URL + transformed_query
    logger.info(f"Requesting : {URL}")
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    return requests.get(URL, headers = headers, timeout = 5)

def search_youtube(query, retries = 4, max_num_results = -1):
    """ Unlimited youtube search by web scrapping """
    transformed_query = reduce(lambda s_ant, s_sig : s_ant + '+' + s_sig, query) if len(query) != 0 else ''
    scrapped_data = []
    num_of_requests = 0
    for i in range(retries):
        page = get_html(transformed_query)
        num_of_requests += 1
        if "</ol>" in page.text:
            break
    logger.info(f" Number of requests : {num_of_requests}")
    soup = BeautifulSoup(page.content, 'html.parser')
    item_list = soup.find('ol', class_='item-section')
    if item_list is None:
        raise Exception(" Html without list of results ")
    items = item_list.find_all('li')
    scrapped_data = [x for x in map(extract_data, items) if x is not None]
    return scrapped_data if max_num_results <= 0 else scrapped_data[:max_num_results]




if __name__ == "__main__":
    import sys
    query = sys.argv[1:]
    scrapped_data = search_youtube(query)
    json_response = json.dumps(scrapped_data)
    json = json.dumps(scrapped_data, indent=2)
    print(json)
