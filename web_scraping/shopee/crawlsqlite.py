from multiprocessing import Process
import pandas as pd
import psutil
import time
# from memory_profiler import profile

from module import output
from module.Categories import Categories
from module import Items

def crawl_tosqlite():
    ## kết nối database
    output_sqlite = 'database.db'
    sqlite_instance = output.Sqlite(output_sqlite)
    conn, cursor = sqlite_instance.conn, sqlite_instance.cursor

    ### ------- crawl Categories ------
    Cats = Categories()

    # Output category. Note, delete old file
    cats_parent = Cats.get_parent()
    sqlite_instance.to_sqlite(input_df=cats_parent, table='categories')

    # # Output SUB_category. Note, delete old file
    cats_children = Cats.get_children()
    sqlite_instance.to_sqlite(input_df=cats_children, table='categories_sub')


    ### ------ Crawl dữ liệu -----

    ## Đọc sub cates từ tệp CSV hiện có:
    cursor.execute('''SELECT * FROM categories_sub''')
    read_data = cursor.fetchall()

    cursor.execute(f"PRAGMA table_info(categories_sub)")
    table_info = cursor.fetchall()
    table_cols = [x[1] for x in table_info]

    sub = pd.DataFrame(read_data,columns=table_cols)

    ## các def
    def memory():
        # Lấy thông tin về bộ nhớ đã sử dụng
        memory_info = psutil.virtual_memory()
        print(f"Percent used: {memory_info.percent}%")
        # print(f"Total memory: {memory_info.total / (1024**3)} Gb")
        print(f"Used memory: {memory_info.used / (1024**3)} Gb")
        print(f"Free memory: {memory_info.available / (1024**3)} Gb")
        return memory_info.available / (1024**3)
        
    def crawl_cat(path, page):
        
        dataCrawl = Items.DetailCat(path=path,page=page)
        # lưu items
        print('--> Đang lưu file KHÔNG ĐƯỢC THOÁT')
        time.sleep(3)
        df_items = dataCrawl.df_items()
        sqlite_instance.to_sqlite(input_df=df_items,table="items")
        
        # lưu shop
        df_shops = dataCrawl.df_shops()
        sqlite_instance.to_sqlite(input_df=df_shops,table="shops")
        
    def crawl_daily(page : int):
        dataCrawl = Items.DetailDaily(page)
        
        print('--> Đang lưu file KHÔNG ĐƯỢC THOÁT')
        df_items = dataCrawl.df_items()
        sqlite_instance.to_sqlite(input_df=df_items,table="items")
        
        df_shops = dataCrawl.df_shops()
        sqlite_instance.to_sqlite(input_df=df_shops,table="shops")
        
    memory_available = memory()
    for i in range(9): # page tối đa 9
        if i <2:
            continue
        if memory_available < 3:
            break
        ## crawl daily
        for j in range(5):
            processDaily = Process(target=crawl_daily, args=(i*10+j,))
            
            processDaily.start()
            processDaily.join()
            
            memory_available = memory()
            print("-->Có thể thoát (5s). Nhấn Ctrl + C ")
            time.sleep(5)
            if memory_available < 3:
                break
            
        ## crawl cate
        for index, row in sub.iterrows(): # lặp qua các sub
            path = row['path']

            processCat = Process(target=crawl_cat, args=(path,i,))

            processCat.start()
            processCat.join()
            
            memory_available = memory()
            print("-->Có thể thoát (5s). Nhấn Ctrl + C")
            time.sleep(5)
            if memory_available < 3:
                break
            
    conn.close()    

# if __name__ == "__main__":
crawl_tosqlite()