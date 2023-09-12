from multiprocessing import Process
import pandas as pd
import os
import time
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
path_dir_out = os.path.join(path_dir,f'output/items.csv')

if os.path.exists(path_dir_out):
    existing_data = pd.read_csv(path_dir_out, low_memory=False)
    print(existing_data.loc[existing_data['cat_subid'].isna()])
    # keyid = existing_data.columns[0]
    # keyid = existing_data.columns[0]
    # duplicates = existing_data[existing_data.duplicated(subset=keyid, keep='first')]
    # print('duplicates')
    # print(duplicates)

    # while existing_data[keyid].duplicated().any():
    #     existing_data = existing_data.drop_duplicates(subset=keyid, keep='first')
    #     duplicates = existing_data[existing_data.duplicated(subset=keyid, keep='first')]
    #     print('duplicates WHILE')
    #     print(duplicates)
    #     existing_data.to_csv(path_dir_out, index=False)
    #     # time.sleep(2)
    #     existing_data = pd.read_csv(path_dir_out, low_memory=False)
    #     print(existing_data[keyid].duplicated().any())
    
    # duplicates = existing_data[existing_data.duplicated(subset=keyid, keep=False)]
    # print('duplicates')
    # print(duplicates)
    
    # path_dir_del = os.path.join(path_dir,f'output/items copy.csv')
    # df_new = pd.read_csv(path_dir_del)
    # keyid = df_new.columns[0]
    # duplicates = df_new[df_new.duplicated(subset=keyid, keep='first')]
    # print(duplicates)
    # time.sleep(2)
    
    # df_new = df_new.drop_duplicates(subset=keyid, keep='first')
    # duplicates = df_new[df_new.duplicated(subset=keyid, keep='first')]
    # print(duplicates)

    