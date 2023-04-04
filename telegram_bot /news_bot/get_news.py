import requests
from bs4 import BeautifulSoup

def get_news():
    request = requests.get('https://vnexpress.net/tin-tuc-24h')
    html_doc = request.text
    lst =[]
    with open('/home/tranlam/Documents/project-python/telegram_bot /news_bot/index.html','r') as f:
        # f.writelines(html_doc)
    
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        tags_with_class_title_news = soup.find_all("h3",{'class': 'title-news'})
        
        i = 0
        for new in tags_with_class_title_news:
            if (i < 10):
                lst.append(new.find('a')["href"])
                i += 1
            else:
                break

    return lst

def main():
    get_news()

        
if __name__ == "__main__":
    main()