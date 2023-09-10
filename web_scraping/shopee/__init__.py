from multiprocessing import Process
import pandas as pd
import os
import psutil
# from memory_profiler import profile

from module import output
from module.Categories import Categories
from module import Items

### ------- crawl Categories ------
# Cats = Categories()

# # Output category. Note, delete old file
# cats_parent = Cats.get_parent()
# output.to_csv(input_df=cats_parent, output_csv='categories.csv')

# # Output SUB_category. Note, delete old file
# cats_children = Cats.get_children()
# output.to_csv(input_df=cats_children, output_csv='categories_sub.csv')


### ------ Crawl dữ liệu -----

# Đọc sub cates từ tệp CSV hiện có:
path_dir=os.path.dirname(__file__)
path_dir_out = os.path.join(path_dir,f'output/categories_sub.csv')

if os.path.exists(path_dir_out):
    sub = pd.read_csv(path_dir_out)
else:
    Cats = Categories()
    cats_children = Cats.get_children()
    output.to_csv(input_df=cats_children, output_csv='categories_sub.csv')
    sub = pd.read_csv(path_dir_out)
    
## crawl từng trang
# @profile
def crawl_cat(path, page):
    
    dataCrawl = Items.DetailCat(path=path,page=page)
        # lưu items
    df_items = dataCrawl.df_items()
    output.to_csv(input_df=df_items,output_csv='items.csv')
    
    # lưu shop
    df_shops = dataCrawl.df_shops()
    output.to_csv(input_df=df_shops,output_csv='shops.csv')
    
    # lưu cates 
    df_cats = dataCrawl.df_cats()
    output.to_csv(input_df=df_cats,output_csv='categories_item.csv')
    
    # Lấy thông tin về bộ nhớ đã sử dụng
    memory_info = psutil.virtual_memory()
    print(f"Percent used: {memory_info.percent}%")
    # print(f"Total memory: {memory_info.total / (1024**3)} Gb")
    print(f"Used memory: {memory_info.used / (1024**3)} Gb")
    print(f"Free memory: {memory_info.available / (1024**3)} Gb")
    
def crawl_daily(page : int):
    dataCrawl = Items.DetailDaily(page)
    
    df_items = dataCrawl.df_items()
    output.to_csv(input_df=df_items,output_csv='items.csv')
    
    df_shops = dataCrawl.df_shops()
    output.to_csv(input_df=df_shops,output_csv='shops.csv')
    
    
for i in range(9): # page tối đa 9
    ## crawl daily
    processDaily = Process(target=crawl_daily, args=(i,))
    
    processDaily.start()
    processDaily.join()
    
    ## crawl cate
    for index, row in sub.iterrows(): # lặp qua các sub
        path = row['path']

        processCat = Process(target=crawl_cat, args=(path,i,))
        
        processCat.start()
        processCat.join()
        
        memory_info = psutil.virtual_memory()
        if memory_info.available / (1024**3) < 2:
            break
        
    memory_info = psutil.virtual_memory()
    if memory_info.available / (1024**3) < 2:
        break
    
        