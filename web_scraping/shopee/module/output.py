import os
import pandas as pd
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
        # Export to csv
        existing_data.to_csv(path_dir_out, index=False)
        
    else:
        # Lưu lại dữ liệu mới vào tệp CSV
        existing_data = input_df.to_csv(path_dir_out, index=False)
        
    print(f"saved to {path_dir_out}")
    return existing_data
    

if __name__ == '__main__':
    pass