# https://shopee.vn/api/v4/pages/get_homepage_category_list
# pip install selenium-wire
from seleniumwire import webdriver
from seleniumwire.utils import decode
import json
import pandas as pd
import time

 # Create a new instance of the Chrome driver
driver = webdriver.Firefox()

# Go to the Google home page
url = 'https://shopee.vn'

driver.get(url)
time.sleep(5)
 
# Access requests via the `requests` attribute
def get():
    for request in driver.requests:
        # print(str(request.url))
        if (str(request.url)) == 'https://shopee.vn/api/v4/pages/get_category_tree':
            #Step 1
            # body = request.response.body
            # print(body)
            
            #Step 2:
            # response = request.response
            # body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
            # print(body)
            
            # #Step 3:
            # response = request.response
            # body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
            # decode_body = body.decode('utf8')
            # print(decode_body)
            
            #Step 4:
            response = request.response
            body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
            decode_body = body.decode('utf8')
            json_data = json.loads(decode_body)
            
            category_list = json_data['data']['category_list']
            categories = [{'display_name':x['display_name'],
                    'catid': x['catid'], 
                    'path': f"{x['display_name'].replace(' ','-')}-cat.{x['catid']}"} for x in category_list]
            
            return categories

if __name__ == '__main__':
    get()