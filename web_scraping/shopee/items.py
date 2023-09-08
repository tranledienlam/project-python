#https://shopee.vn/Th%E1%BB%9Di-Trang-Tr%E1%BA%BB-Em-cat.11036382?page=0

from seleniumwire import webdriver
from seleniumwire.utils import decode
from datetime import datetime
import pandas as pd
import json
import time
# def path_list(page=1):
#     options = webdriver.FirefoxOptions()
#     options.headless = True

#     driver = webdriver.Firefox(options=options)

#     url = f'https://shopee.vn/daily_discover?pageNumber={page}'

#     driver.get(url)
#     time.sleep(3)
    
#     for request in driver.requests:
#         # print(str(request.url))
#         if (str(request.url)).startswith('https://shopee.vn/api/v4/homepage/get_daily_discover?bundle'):

#             response = request.response
#             body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
#             decode_body = body.decode('utf8')
#             json_data = json.loads(decode_body)
            
#             items_feeds = json_data['data']['feeds']#['item_card']['item']
#             items_list = [x['item_card']['item'] for x in items_feeds]
#             path_items = [{
#                             'name': re.sub(r'[^\w^" "]','',x['name']),
#                             'itemid': x['itemid'],
#                             'shopid': x['shopid']
#                             } for x in items_list]
#             path = [ f"{x['name'].replace(' ','-')}-i.{x['shopid']}.{x['itemid']}" for x in path_items]
#             print(path)
#             return path

#     driver.quit()
    
def detail_cat(path: str,page = 0):
    cat_subid = path.split('.')[-1]
    
    options = webdriver.FirefoxOptions()
    options.headless = True
    # options = {
    #             'proxy': {
    #                 'http': 'http://78.47.11.34:20009',
    #                 'https': 'http://78.47.11.34:20009',
    #                 'custom_authorization': 'elite proxy'
    #             }
    #         }
    driver = webdriver.Firefox(options=options)
    # driver.proxy = {
    #     'https': 'https://144.49.99.169:8080',
    # }
    url = f'https://shopee.vn/{path}?page={page}'

    driver.get(url)

    time.sleep(3)
    
    for request in driver.requests:
        # print(str(request.url))
        if (str(request.url)).startswith('https://shopee.vn/api/v4/recommend/recommend?bundle'):

            response = request.response
            body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
            decode_body = body.decode('utf8')
            json_data = json.loads(decode_body)
            
            items_data = json_data['data']['sections'][0]['data']['item']#['item_card']['item']
            items = [{
                        "itemid": i['itemid'],
                        "name": i["name"],
                        "cat_itemid": i["catid"],
                        "cat_subid": cat_subid,
                        "price_min": str(i["price_min"])[:-5],
                        "price_max": str(i["price_min"])[:-5],
                        "price_min_before_discount": str(i["price_min_before_discount"])[:-5],
                        "price_max_before_discount": str(i["price_max_before_discount"])[:-5],
                        "discount": i["discount"],
                        "historical_sold": i["historical_sold"],
                        "liked_count": i["liked_count"], # số người like sản phẩm
                        "item_rating_star": i["item_rating"]["rating_star"],
                        "item_rating_count": i["item_rating"]["rating_count"][0],
                        "item_rating_count_star1": i["item_rating"]["rating_count"][1],
                        "item_rating_count_star2": i["item_rating"]["rating_count"][2],
                        "item_rating_count_star3": i["item_rating"]["rating_count"][3],
                        "item_rating_count_star4": i["item_rating"]["rating_count"][4],
                        "item_rating_count_star5": i["item_rating"]["rating_count"][5],
                        "item_rcount_with_image": i["item_rating"]["rcount_with_image"],
                        "item_rcount_with_context": i["item_rating"]["rcount_with_context"],
                        "ctime": datetime.fromtimestamp(i["ctime"]).strftime('%Y-%m-%d %H:%M:%S'),
                        "shopid": i['shopid'],
                        "shop_name": i["shop_name"],
                        "shopee_verified": i["shopee_verified"],
                        "shop_location": i["shop_location"],
                        "shop_rating": i["shop_rating"],
                    } for i in items_data]
            df = pd.DataFrame(items)
            
            return df

    time.sleep(10)
    driver.quit()
if __name__ == '__main__':
    
    path = 'Áo-Khoác-cat.11035567.11035568'
    detail_cat(path, page=2)
    