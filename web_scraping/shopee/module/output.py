import os
import pandas as pd
import numpy as np
import time
import _sqlite3
# from memory_profiler import profile

# @profile
def to_csv(input_df: pd.DataFrame, output_csv : str = 'data.csv'):
    if input_df is None:
        return None
    
    if type(input_df) == list:
        input_df = pd.DataFrame(input_df)
        
    # Đặt tên cho file CSV
    curr_dir=os.path.dirname(__file__)
    parent_dir =os.path.dirname(curr_dir)
    path_dir_out = os.path.join(parent_dir,f'output/{output_csv}')
    
    # Đọc dữ liệu từ tệp CSV hiện có vào DataFrame
    if os.path.exists(path_dir_out):
        existing_data = pd.read_csv(path_dir_out, low_memory=False)
        
        # # Kiểm tra và thêm dữ liệu mới vào DataFrame
        keyid = existing_data.columns[0]
        # existing_data = pd.concat([input_df, existing_data[~existing_data[keyid].isin(input_df[keyid])]], ignore_index=True)
        # existing_data.to_csv(path_dir_out, index=False)

        existing_data.set_index(keyid, inplace=True)
        input_df.set_index(keyid, inplace=True)
        
        # Cập nhật existing_data từ input_df
        for index, row in input_df.iterrows():
            if index in existing_data.index:

                # Cập nhật các giá trị khác nhau từ input_df vào existing_data, trừ trường hợp giá trị là None (NaN)
                for col in input_df.columns:
                    if not pd.isna(row[col]):
                        existing_data.loc[index, col] = row[col]
            else:
                # Thêm dòng từ input_df vào existing_data nếu không tồn tại
                existing_data = pd.concat([existing_data, row.to_frame().T])

        # Đặt lại cột keyid
        existing_data.reset_index(inplace=True)
        existing_data = existing_data.rename(columns={'index': keyid}) 

        # Xử lý duplicate
        while existing_data[keyid].duplicated().any():
            print(f'Xử lý duplicates {output_csv}')
            existing_data = existing_data.drop_duplicates(subset=keyid, keep='last')
            existing_data.to_csv(path_dir_out, index=False)
            time.sleep(3)
            existing_data = pd.read_csv(path_dir_out, low_memory=False)
        # Export to csv
        else:
            existing_data.to_csv(path_dir_out, index=False)
        
    else:
        # Lưu lại dữ liệu mới vào tệp CSV
        existing_data = input_df.to_csv(path_dir_out, index=False)
        
    print(f"saved to {path_dir_out}")
    return existing_data
    


def check_if_lid_exists(keyname, keyid, table, cursor):
    # Sử dụng câu truy vấn SQL để kiểm tra xem giá trị lid đã tồn tại
    print(f"SELECT COUNT(*) FROM {table} WHERE {keyname} = {keyid}")
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {keyname} = {keyid}")
    count = cursor.fetchone()[0]
    return count > 0


def conn_sqlite(output_sqlite: str):
    
    # Kết nối đến cơ sở dữ liệu hoặc tạo nếu nó chưa tồn tại
    curr_dir=os.path.dirname(__file__)
    parent_dir =os.path.dirname(curr_dir)
    path_dir_out = os.path.join(parent_dir,f'output/{output_sqlite}')
    conn = _sqlite3.connect(path_dir_out)

    # Tạo một đối tượng cursor để thực thi truy vấn SQL
    cursor = conn.cursor()

    # Tạo bảng (nếu nó chưa tồn tại)
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        itemid INTEGER PRIMARY KEY,
                        cat_itemid INTEGER,
                        cat_subid INTEGER,
                        shopid INTEGER,
                        name TEXT,
                        price_min INTEGER,
                        price_max INTEGER,
                        price_min_before_discount INTEGER,
                        price_max_before_discount INTEGER,
                        discount TEXT,
                        historical_sold INTEGER,
                        liked_count INTEGER,
                        item_rating_star REAL,
                        item_rating_count REAL,
                        item_rating_count_star1 REAL,
                        item_rating_count_star2 REAL,
                        item_rating_count_star3 REAL,
                        item_rating_count_star4 REAL,
                        item_rating_count_star5 REAL,
                        item_rcount_with_image REAL,
                        item_rcount_with_context REAL,
                        ctime TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS shops (
                        shopid INTEGER PRIMARY KEY,
                        shop_name TEXT,
                        shop_location TEXT,
                        shop_rating REAL,
                        shopee_verified INTEGER,
                        Shopdacbiet INTEGER,
                        Shopxuhuong INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                        catid INTEGER PRIMARY KEY,
                        cat_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories_sub (
                        cat_subid INTEGER PRIMARY KEY,
                        cat_sub_name TEXT,
                        catid INTEGER,
                        path TEXT)''')
    return conn, cursor
    
def to_sqlite(input_df: pd.DataFrame, output_sqlite: str, table):
    conn, cursor = conn_sqlite(output_sqlite)
    
    if input_df is None:
        return None
    
    if type(input_df) == list:
        input_df = pd.DataFrame(input_df)
        
    # sắp xếp trường của input_df đúng với thức tự database
    cursor.execute(f"PRAGMA table_info({table})")
    table_info = cursor.fetchall()
    table_cols = [x[1] for x in table_info]
    
    placeholders = ', '.join(['?'] * len(input_df.columns))
    insert_query = f"INSERT INTO {table} VALUES ({placeholders})"
    for index, row in input_df[table_cols].iterrows():
        time.sleep(0.1)
        try:    
            insert_data = tuple(row.values)
            cursor.execute(insert_query,insert_data)
            conn.commit()

        except _sqlite3.IntegrityError as error:
            col_not_none = [f'{keyname} = ?' for keyname in table_cols if row[keyname] != None]
            str_query = ', '.join(col_not_none[1:])
            
            value = [row[keyname] for keyname in table_cols if row[keyname] != None]
            update_value = tuple(value[1:]+[value[0]])
            print(f"update {table} {value[0]}")
            update_query = f"UPDATE {table} SET {str_query} WHERE {table_cols[0]} = ?"
            
            cursor.execute(update_query, update_value)
            conn.commit()
        except Exception as error:
            print(f'to_splite: {error}')

    print('Đã update database')
    conn.close()

__all__ = ["to_csv","to_sqlite"]
