import time
from datetime import datetime
import random
item_daily_discover = {
  "itemid": 3891290785,
  "shopid": 460257458,
  "name": "Áo Khoác Gió Nam Nữ, ÁO KHOÁC Gió 2 Lớp Nam Nữ (Ảnh Thật/như hình) D30",
  "ctime": 1623080468,
  "sold": 724,
  "historical_sold": 12261,
  "liked_count": 12953,  
  "catid": 100011,
  "price": 8900000000,
  "price_min": 8900000000,
  "price_max": 9900000000,
  "price_min_before_discount": 12900000000,
  "price_max_before_discount": 12900000000,
  "discount": "31%",
  "item_rating": {
    "rating_star": 4.723315774882174,
    "rating_count": [
      3608, 
      37,
      38,
      183,
      373,
      2977 
    ],
    "rcount_with_image": 717, 
    "rcount_with_context": 1462 
  },
  "shopee_verified": True,
  "shop_location": "TP. Hồ Chí Minh",
  "shop_rating": 4.701711,
}

print(str(item_daily_discover["item_rating"]["rating_count"][5]))
print(time.ctime(item_daily_discover["ctime"]))
print(str(1)[:-5])
print(datetime.fromtimestamp(1623080468).strftime('%Y-%m-%d %H:%M:%S'))
path = 'Áo-Khoác-cat.11035567.11035568'
print(path.split('.')[-1])
print(random.choice)
