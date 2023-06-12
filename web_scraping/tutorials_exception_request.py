import requests
import logging
import httpx

logging.basicConfig(filename='/home/tranlam/Documents/project-python/web_scraping/showlog.log', format='%(asctime)s %(message)s',
                    encoding='UTF-8', level=logging.WARNING)

try:
    r = requests.get('https://google.com/')
    r.raise_for_status()
    logging.warning(r.raise_for_status())
except requests.exceptions.RequestException as err:
    logging.warning(err)
    print('Request Exception')
