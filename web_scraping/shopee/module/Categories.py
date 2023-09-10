# https://shopee.vn/api/v4/pages/get_homepage_category_list
# pip install selenium-wire
from seleniumwire import webdriver
from seleniumwire.utils import decode
import json
import time
import re

# Access requests via the `requests` attribute
class Categories:
    def __init__(self) -> None:
        self.cats_all = None
        print('--> crawling Categories -->')
        
        try:
            # Create a new instance of the Chrome driver
            options = webdriver.FirefoxOptions()
            options.headless = True
            
            driver = webdriver.Firefox(options=options)

            # Go to shopee
            url = 'https://shopee.vn'

            driver.get(url)
            time.sleep(5)
            
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
                    # print(category_list)
                    categories = [{
                                    'catid': str(x['catid']),
                                    'cat_name': x['display_name'],
                                    'sub_cats': [ {
                                                    'cat_subid': str(y['catid']),
                                                    'cat_sub_name': y['display_name'],
                                                    'catid': str(y['parent_catid']),
                                                    'path': re.sub(r'[-\W]+', '-', y["display_name"]).strip('-')+f'-cat.{y["parent_catid"]}.{y["catid"]}'
                                                } for y in x['children']]
                                    # 'path': f"{x['display_name'].replace(' ','-')}-cat.{x['catid']}"
                                } for x in category_list]

                    self.cats_all = categories
            driver.quit()
            print('-- End crawl --')
        except:
            print("xử lý bị lỗi")

    
    def get_parent(self):
        cats_parent = [{
                        'catid':x['catid'],
                        'cat_name': x['cat_name']
                        } for x in self.cats_all]
        
        return cats_parent

    def get_children(self):
        cats_sub =[]
        for i in range(len(self.cats_all)):
            cats_sub+=self.cats_all[i]['sub_cats']

        return cats_sub
