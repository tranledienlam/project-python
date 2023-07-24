from bs4 import BeautifulSoup
import os
import re
import requests

url = 'https://coinmarketcap.com/'
result = requests.get(url).text
doc = BeautifulSoup(result,'html.parser')

tbody = doc.tbody
trs = (tbody.contents)

prices = {}

for tr in trs[:10]:
    name, price =  tr.contents[2:4]
    name = name.p.string
    price = price.span.text
    prices[name] = price

print(prices)

# with open('/home/tranlam/Documents/project-python/web_crawler/index2.html','r') as f:
#     soup = BeautifulSoup(f, "html.parser")

# tag_bt = soup.find(class_='btn-group')
# print(tag_bt)

# print(list(tag_bt.children))
# for chil in tag_bt.children:
#     print(chil)
    
# print(list(tag_bt.descendants))

# for chil in tag_bt.descendants:
#     print(chil)
# # # Print all the descendants of tag
# # for descendant in soup.children:
# #     print(descendant)
