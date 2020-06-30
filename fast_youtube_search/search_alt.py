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
    data = call_api(query)    
    return data if max_num_results <= 0 else data[:max_num_results]

def transform_query(query):
    return reduce(lambda s_ant, s_sig : s_ant + '+' + s_sig, query) if len(query) != 0 else ''

def call_api(query):
    BASE_URL = 'https://www.youtube.com/results?search_query='
    URL = BASE_URL + transform_query(query) + '&pbj=1'
    logger.info(f"Requesting : {URL}")
    headers = {
    'authority': 'www.youtube.com',
     'pragma': 'no-cache' ,
     'cache-control': 'no-cache' ,
     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' ,
     'x-spf-referer': 'https://www.youtube.com/' ,
     'x-youtube-utc-offset': '-300' ,
     'x-youtube-client-name': '1' ,
     'x-spf-previous': 'https://www.youtube.com/' ,
     'x-youtube-client-version': '2.20200627.05.01' ,
     'accept': '*/*' ,
     'sec-fetch-site': 'same-origin' ,
     'sec-fetch-mode': 'cors' ,
     'sec-fetch-dest': 'empty' ,
     'referer': 'https://www.youtube.com/' ,
     'accept-language': 'en-US,en;q=0.9,es;q=0.8' ,
    }
    response = requests.get(URL, headers = headers, timeout = 5).json()
    results  = response[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    results = [ extract_data_api(video) for video in results ]
    results = [r for r in results if r is not None ]
    return results

def extract_data_api(video)  :
    if 'videoRenderer' not in video:
        return
    video_id = video['videoRenderer']['videoId']
    return {
        'name': video['videoRenderer']['title']['runs'][0]['text'],
        'id': video_id,
        'img': 'https://i.ytimg.com/vi/' + video_id + '/hqdefault.jpg'
    }




if __name__ == "__main__":
    import sys
    query = sys.argv[1:]
    # scrapped_data = search_youtube(query)
    # json_response = json.dumps(scrapped_data)
    # json = json.dumps(scrapped_data, indent=2)
    # print(json)
    res = search_youtube(query)
    print(res)
