import pandas as pd
import os
import random

import categories
import output
import items

### Output category. Note, delete old file
# cats_parent = categories.get_parent()
# output.to_csv(input_df=cats_parent, output_csv='categories.csv')

### Output SUB_category. Note, delete old file
# cats_children = categories.get_children()
# output.to_csv(input_df=cats_children, output_csv='subcategories.csv')


### Crawl dữ liệu
path_dir=os.path.dirname(__file__)
path_dir_out = os.path.join(path_dir,f'output/subcategories.csv')
# Đọc dữ liệu từ tệp CSV hiện có vào DataFrame
if os.path.exists(path_dir_out):
    sub = pd.read_csv(path_dir_out)
else:
    cats_children = categories.get_children()
    output.to_csv(input_df=cats_children, output_csv='subcategories.csv')
    sub = pd.read_csv(path_dir_out)
# crawl theo danh sách file
for index, row in sub.iterrows():
    path = row['path']
    pages = random.choice([7,8,9,10])
    for i in range(pages):
        itemsDetail = items.detail_cat(path, page=i)
        output.to_csv(input_df=itemsDetail,output_csv='products.csv')