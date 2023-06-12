from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# url = 'https://the-internet.herokuapp.com/login'
# driver.get(url)

# # //*[@id="username"]
# # //*[@id="password"]  
# # //*[@id="login"]/button
# time.sleep(1)
# input_name = 'tomsmith'
# input_password = 'SuperSecretPassword!'

# for i in input_name:
#     driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(i)
#     time.sleep(0.1)
# time.sleep(1)

# for i in input_password:    
#     driver.find_element(By.XPATH,'//*[@id="password"]  ').send_keys(i)
#     time.sleep(0.1)
# time.sleep(1)

# driver.find_element(By.XPATH,'//*[@id="login"]/button').click()

#---------------
# url = 'https://the-internet.herokuapp.com/dynamic_loading/2'

# driver.get(url)
# # //*[@id="start"]/button
# # //*[@id="finish"]/h4

# driver.find_element(By.XPATH,'//*[@id="start"]/button').click()

# driver.implicitly_wait(10)

# text = driver.find_element(By.XPATH,'//*[@id="finish"]/h4').text

# print(text)

# -------------------
url = 'https://www.youtube.com/@JohnWatsonRooney/videos'

driver.get(url)
# style-scope ytd-rich-grid-media
# //*[@id="video-title"]
# //*[@id="metadata-line"]/span[1]
# //*[@id="metadata-line"]/span[2]

videos = driver.find_elements(By.CLASS_NAME,'style-scope ytd-rich-grid-media')
videos_list = []

for video in videos:
    title = video.find_element(By.XPATH,'.//*[@id="video-title"]').text
    view = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[1]').text
    when = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text
    
    video_item = {
        'title': title,
        "views": view,
        'posted': when
    }
    
    videos_list.append(video_item)
    
df = pd.DataFrame(videos_list)
print(df)

time.sleep(60)
driver.quit()
