import pandas as pd
import numpy as np

# Tạo DataFrame a
data_a = [{'id': 1, 'name': 'John', 'age': 30},
          {'id': 2, 'name': 'Alice', 'age': None},
          {'id': 3, 'name': 'Bob', 'age': 28}]
a = pd.DataFrame(data_a)

# Tạo DataFrame b
data_b = [{'id': 1, 'name': 'John', 'age': 100},
          {'id': 2, 'name': 'Alice', 'age': 25},
          {'id': 3, 'name': 'Charlie', 'age': None},
          {'id': 4, 'name': 'Eve', 'age': 22}]
b = pd.DataFrame(data_b)

# Đặt cột 'id' làm index cho cả hai DataFrame
a.set_index('id', inplace=True)
b.set_index('id', inplace=True)
# print(a)
# Cập nhật a từ b
for index, row in b.iterrows():
    if index in a.index:

        # Cập nhật các giá trị khác nhau từ b vào a, trừ trường hợp giá trị là None (NaN)
        for col in b.columns:
            if not pd.isna(row[col]):
                a.loc[index, col] = row[col]
    else:
        # Thêm dòng từ b vào a nếu không tồn tại
        a = pd.concat([a, row.to_frame().T])
        print(a)
# Đặt lại cột 'id' thành cột
a.reset_index(inplace=True)
a.rename(columns={'index': 'Categories'})
print(a)
# Hiển thị kết quả
# print(a)
