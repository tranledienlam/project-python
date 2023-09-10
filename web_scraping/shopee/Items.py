#https://shopee.vn/Th%E1%BB%9Di-Trang-Tr%E1%BA%BB-Em-cat.11036382?page=0

from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from memory_profiler import profile

from datetime import datetime
import pandas as pd
import json
import time
import re

def config_driver():
    options = webdriver.FirefoxOptions()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    
    return driver

class DetailCat:
    # @profile
    def __init__(self, path: str, page: int = 0) -> None:
        """
        path: string categories 'Áo-Khoác-cat.11035567.11035568'
        page: [0-8] tương đương từ trang thứ 1 đến trang thứ 9
        """
        self.details = None
        
        print(f"-- crawling sub: {path} - page: {page} --")
        cat_subid = path.split('.')[-1]
        
        attempts = 0
        while attempts < 2:
            try:
                options = webdriver.FirefoxOptions()
                options.headless = True

                driver = webdriver.Firefox(options=options)
                
                # driver.proxy = {
                #     'https': 'https://144.49.99.169:8080',
                # }
                url = f'https://shopee.vn/{path}?page={page}'

                driver.get(url)

                # Đợi cho đến khi điều kiện nào đó xuất hiện trên trang (ví dụ: element có ID 'some_element')
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'div'))
                )
                
                time.sleep(3)
                
                for request in driver.requests:
                
                    if (str(request.url)).startswith('https://shopee.vn/api/v4/recommend/recommend?bundle'):

                        response = request.response
                        body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
                        decode_body = body.decode('utf8')
                        json_data = json.loads(decode_body)
                        items_data = json_data['data']['sections'][0]['data']['item']
                        
                        items = [{
                                "itemid": i['item_card']['item']['itemid'],
                                "name": re.sub(r'\r', '', i["name"]),
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

                        print(df.head(2))
                        self.details = df
                        
            except TimeoutException:
                # Xử lý nếu timeout xảy ra
                print("Timeout: Không thể tải trang trong thời gian quy định 20s.")
                break
            except Exception as e:
                print(f"Lỗi: {e}")
                attempts += 1 
                # Chờ một khoảng thời gian trước khi thử lại
                time.sleep(20)
            else:
                break
            finally:
                driver.quit()
    # @profile
    def df_items(self):
        if self.details is None:
            return None
        
        df_items = self.details[[
                            "itemid",
                            "cat_itemid",
                            "shopid",
                            "name",
                            "price_min",
                            "price_max",
                            "price_min_before_discount",
                            "price_max_before_discount",
                            "discount",
                            "historical_sold",
                            "liked_count",
                            "item_rating_star",
                            "item_rating_count",
                            "item_rating_count_star1",
                            "item_rating_count_star2",
                            "item_rating_count_star3",
                            "item_rating_count_star4",
                            "item_rating_count_star5",
                            "item_rcount_with_image",
                            "item_rcount_with_context",
                            "ctime"
                          ]]
        df_items = df_items.copy()
        df_items.reset_index(drop=True, inplace=True)
        
        keyid = df_items.columns[0]
        df_items.drop_duplicates(subset=keyid, keep="last", inplace=True)
        
        return df_items
    # @profile
    def df_shops(self):
        if self.details is None:
            return None
        df_shops = self.details[["shopid",
                              "shop_name",
                              "shop_location",
                              "shop_rating",
                              "shopee_verified"
                              ]]
        
        df_shops = df_shops.copy()
        df_shops.reset_index(drop=True, inplace=True)
        
        keyid = df_shops.columns[0]
        df_shops.drop_duplicates(subset=keyid, keep="last", inplace=True)
        return df_shops
    # @profile
    def df_cats(self):
        if self.details is None:
            return None
        # tạo copy slice từ gốc, giải quyết vấn đề "A value is trying to be set on a copy of a slice from a DataFrame"
        # do cố gắng drop từ df gốc
        df_cats = self.details[["cat_itemid",
                             "cat_subid"]]
        
        df_cats = df_cats.copy()
        df_cats.reset_index(drop=True, inplace=True)
        
        keyid = df_cats.columns[0]
        df_cats.drop_duplicates(subset=keyid, keep="last", inplace=True)
        
        return df_cats

class DetailDaily:
    # @profile
    def __init__(self, page: int = 0) -> None:
        """
        page: [1-] tương đương từ trang thứ 1 đến trang N (không giới hạn)
        """
        self.details = None
        
        print(f"-- crawling Daily: page: {page} --")
        
        attempts = 0
        while attempts < 2:
            try:
                # options = webdriver.FirefoxOptions()
                # options.headless = True

                # driver = webdriver.Firefox(options=options)
                driver = config_driver()
                # driver.proxy = {
                #     'https': 'https://144.49.99.169:8080',
                # }
                url = f'https://shopee.vn/daily_discover?pageNumber={page}'

                driver.get(url)

                # Đợi cho đến khi điều kiện nào đó xuất hiện trên trang (ví dụ: element có ID 'some_element')
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'div'))
                )
                
                time.sleep(3)
                
                for request in driver.requests:
                    if (str(request.url)).startswith('https://shopee.vn/api/v4/homepage/get_daily_discover?bundle'):
                        print(request.url)

                        response = request.response
                        body = decode(response.body,response.headers.get('Content-Encoding','Identity'))
                        decode_body = body.decode('utf8')
                        json_data = json.loads(decode_body)
                        items_data = json_data['data']['feeds']#['item_card']['item']
                        
                        
                        items = [{
                                "itemid": i['item_card']['item']['itemid'],
                                "name": re.sub(r'\r', '', i['item_card']['item']["name"]),
                                "cat_itemid": i['item_card']['item']["catid"],
                                "cat_subid": None,
                                "price_min": str(i['item_card']['item']["price_min"])[:-5],
                                "price_max": str(i['item_card']['item']["price_min"])[:-5],
                                "price_min_before_discount": str(i['item_card']['item']["price_min_before_discount"])[:-5],
                                "price_max_before_discount": str(i['item_card']['item']["price_max_before_discount"])[:-5],
                                "discount": i['item_card']['item']["discount"],
                                "historical_sold": i['item_card']['item']["historical_sold"],
                                "liked_count": i['item_card']['item']["liked_count"], # số người like sản phẩm
                                "item_rating_star": i['item_card']['item']["item_rating"]["rating_star"],
                                "item_rating_count": i['item_card']['item']["item_rating"]["rating_count"][0],
                                "item_rating_count_star1": i['item_card']['item']["item_rating"]["rating_count"][1],
                                "item_rating_count_star2": i['item_card']['item']["item_rating"]["rating_count"][2],
                                "item_rating_count_star3": i['item_card']['item']["item_rating"]["rating_count"][3],
                                "item_rating_count_star4": i['item_card']['item']["item_rating"]["rating_count"][4],
                                "item_rating_count_star5": i['item_card']['item']["item_rating"]["rating_count"][5],
                                "item_rcount_with_image": i['item_card']['item']["item_rating"]["rcount_with_image"],
                                "item_rcount_with_context": i['item_card']['item']["item_rating"]["rcount_with_context"],
                                "ctime": datetime.fromtimestamp(i['item_card']['item']["ctime"]).strftime('%Y-%m-%d %H:%M:%S'),
                                "shopid": i['item_card']['item']['shopid'],
                                "shop_name": i['item_card']['item']["shop_name"],
                                "shopee_verified": i['item_card']['item']["shopee_verified"],
                                "shop_location": i['item_card']['item']["shop_location"],
                                "shop_rating": i['item_card']['item']["shop_rating"],
                            } for i in items_data]
                        # df = pd.DataFrame(items)
                        print(items)
                        # print(df.head(2))
                        # self.details = df
                        
            except TimeoutException:
                # Xử lý nếu timeout xảy ra
                print("Timeout: Không thể tải trang trong thời gian quy định 20s.")
                break
            except Exception as e:
                print(f"Lỗi: {e}")
                attempts += 1 
                # Chờ một khoảng thời gian trước khi thử lại
                time.sleep(20)
            else:
                break
            finally:
                driver.quit()
    # @profile
    def df_items(self):
        if self.details is None:
            return None
        
        df_items = self.details[[
                            "itemid",
                            "cat_itemid",
                            "shopid",
                            "name",
                            "price_min",
                            "price_max",
                            "price_min_before_discount",
                            "price_max_before_discount",
                            "discount",
                            "historical_sold",
                            "liked_count",
                            "item_rating_star",
                            "item_rating_count",
                            "item_rating_count_star1",
                            "item_rating_count_star2",
                            "item_rating_count_star3",
                            "item_rating_count_star4",
                            "item_rating_count_star5",
                            "item_rcount_with_image",
                            "item_rcount_with_context",
                            "ctime"
                          ]]
        df_items = df_items.copy()
        df_items.reset_index(drop=True, inplace=True)
        
        keyid = df_items.columns[0]
        df_items.drop_duplicates(subset=keyid, keep="last", inplace=True)
        
        return df_items
    # @profile
    def df_shops(self):
        if self.details is None:
            return None
        df_shops = self.details[["shopid",
                              "shop_name",
                              "shop_location",
                              "shop_rating",
                              "shopee_verified"
                              ]]
        
        df_shops = df_shops.copy()
        df_shops.reset_index(drop=True, inplace=True)
        
        keyid = df_shops.columns[0]
        df_shops.drop_duplicates(subset=keyid, keep="last", inplace=True)
        return df_shops
