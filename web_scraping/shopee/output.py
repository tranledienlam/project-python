import os
import pandas as pd

def to_csv(input_df: pd.DataFrame, output_csv : str = 'data.csv'):
    
    if type(input_df) == list:
        input_df = pd.DataFrame(input_df)
        
    # Đặt tên cho file CSV
    path_dir=os.path.dirname(__file__)
    path_dir_out = os.path.join(path_dir,f'output/{output_csv}')
    
    # Đọc dữ liệu từ tệp CSV hiện có vào DataFrame
    if os.path.exists(path_dir_out):
        existing_data = pd.read_csv(path_dir_out)
        
        # Kiểm tra và thêm dữ liệu mới vào DataFrame
        keyid = existing_data.columns[0]
        existing_data = pd.concat([input_df, existing_data[~existing_data[keyid].isin(existing_data[keyid])]], ignore_index=True)
        existing_data.to_csv(path_dir_out, index=False)
    else:
        # Lưu lại dữ liệu mới vào tệp CSV
        input_df.to_csv(path_dir_out, index=False)
    

if __name__ == '__main__':
    pass