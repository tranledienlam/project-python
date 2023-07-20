# https://the-internet.herokuapp.com/authenticate
# https://the-internet.herokuapp.com/secure

import requests
from bs4 import BeautifulSoup

loginurl = 'https://the-internet.herokuapp.com/authenticate'
secureurl = 'https://the-internet.herokuapp.com/secure'
payload = {
    'username': 'tomsmith',
    'password': 'SuperSecretPassword!'
}

with requests.session() as s:
    
    r = s.post(loginurl,data=payload)
    r2 = s.get(secureurl)
    soup = BeautifulSoup(r2.content,'html.parser')
    
print(r2.text)