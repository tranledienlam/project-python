from multiprocessing import Process
import pandas as pd
import os
import psutil
import time
# from memory_profiler import profile

from module import output
from module.Categories import Categories
from module import Items

# df_items = pd.DataFrame({
#     "itemid": [8217220197],
#     "cat_itemid": [100017],
#     "shopid": [378384270],
#     "name": ['(Hàng có sẵn) Quần biker short']
# })
# df_shop = pd.DataFrame({
#     "shop_name":["Choco12"],
#     "shopid":[37884212320],
#     "shop_location":[None]
# })
path = 'Áo-Khoác-cat.11035567.11035568'
dataCrawl = Items.DetailCat(path=path,page=0)
df_items = dataCrawl.df_items()
output.to_sqlite(input_df=df_items, output_sqlite='database.db',table="items")
# print(df_shop)