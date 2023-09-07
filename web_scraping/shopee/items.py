#https://shopee.vn/Th%E1%BB%9Di-Trang-Tr%E1%BA%BB-Em-cat.11036382?page=0

from seleniumwire import webdriver
from seleniumwire.utils import decode
import json
import pandas as pd
import time

driver = webdriver.Firefox()

# Go to the Google home page
url = 'https://shopee.vn/Th%E1%BB%9Di-Trang-Tr%E1%BA%BB-Em-cat.11036382?page=0'

driver.get(url)
time.sleep(5)

def get():
    for request in driver.requests:
        # print(str(request.url))
        if (str(request.url)).startswith('https://shopee.vn/api/v4/recommend/recommend?bundle'):

            response = request.response
            body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
            decode_body = body.decode('utf8')
            json_data = json.loads(decode_body)
            
            items_list = json_data['data']['sections'][0]['data']['item']
            # categories = [{'display_name':x['display_name'],
            #         'catid': x['catid'], 
            #         'path': f"{x['display_name'].replace(' ','-')}-cat.{x['catid']}"} for x in category_list]
            print(items_list)
            # return categories

# if __name__ == '__main__':
get()