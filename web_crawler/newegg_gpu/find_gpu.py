from bs4 import BeautifulSoup
import requests
import os
import time

gpu = 'intel'

url = f'https://www.newegg.com/p/pl?d={gpu}&page=1'
page = requests.get(url).text
doc = BeautifulSoup(page,'html.parser')

page_text = doc.find(class_='list-tool-pagination-text').strong

pages = int(str(page_text.text).split('/')[-1])

items_found = {}
stt = 0

path_dir = os.path.dirname(__file__)
save_file = os.path.join(path_dir,'data.csv')


if os.path.exists(save_file):
    os.remove(save_file)
    f= open(save_file,'a')
else:
    f=open(save_file,'a')
    first_line='name,price,link\n'
    f.write(first_line)
for page in range(pages):
    url = f'https://www.newegg.com/p/pl?d={gpu}&page={page+1}'
    page = requests.get(url).text
    doc = BeautifulSoup(page,'html.parser')

    items = doc.find_all(class_='item-cell')
    for item in items:
        try:
            # link
            tag_a = item.find('a')
            link = tag_a['href']
            #name
            name = tag_a.img['title']
            name = name.replace(',', '-')
            # price
            tag_li = item.find('li', class_='price-current')
            price_int = tag_li.strong.text
            price_int = price_int.replace(',', ' ')
            price_decimal = tag_li.sup.text
            price = f"${price_int}{price_decimal}"

            items_found[name] = {"price": price, "link":link}
            stt +=1
            # write to csv
            line = f'{name},{price},{link}\n'
            f.write(line)
            print(f'''
STT-{stt}{'-'*10}
{name}
{price}
{link}                  
                  ''')
            time.sleep(0.1)
        except:
            pass    
f.close()        

