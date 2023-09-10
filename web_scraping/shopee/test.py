from multiprocessing import Process
import pandas as pd
import os
import random
import psutil
# import time
# from memory_profiler import profile

import output
from Categories import Categories
from Items import DetailCat

### ------- crawl Categories ------
# Cats = Categories()

## Output category. Note, delete old file
# cats_parent = Cats.get_parent()
# output.to_csv(input_df=cats_parent, output_csv='categories.csv')

## Output SUB_category. Note, delete old file
# cats_children = Cats.get_children()
# output.to_csv(input_df=cats_children, output_csv='categories_sub.csv')


### ------ Crawl dữ liệu -----

## Đọc sub cates từ tệp CSV hiện có:
path_dir=os.path.dirname(__file__)
path_dir_out = os.path.join(path_dir,f'output/items.csv')

if os.path.exists(path_dir_out):
    sub = pd.read_csv(path_dir_out)
else:
    Cats = Categories()
    cats_children = Cats.get_children()
    output.to_csv(input_df=cats_children, output_csv='categories_sub.csv')
    sub = pd.read_csv(path_dir_out)
print(sub['itemid'])
# Lỗi: LookupError when decoding b'{"bff_me with 'Identity': LookupError('unknown encoding: Identity')
Không tồn tại sản phẩm
