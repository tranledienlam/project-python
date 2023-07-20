import requests
from requests.utils import dict_from_cookiejar

class login():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.s = requests.session()
        # self.s.trust_env == False
        headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://tuongtaccheo.com/index.php",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE":"trailers",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        self.s.headers.update(headers)
        data = {
            "username": self.username, #"hayashibutler",
            "password":	self.password, #"654321",
            "submit": "ĐĂNG+NHẬP"
        }
        login_res = self.s.post('https://tuongtaccheo.com/login.php', timeout=10, data=data)
        
        # self.s.cookies.clear_session_cookies()
        # print(self.s.cookies)
        # self.cookies_dict = dict_from_cookiejar(self.login_res.cookies)

    def get_cookies(self):
        return self.s.cookies.get_dict()
    
    def check_xu(self):
        self.getXu = self.s.get('https://tuongtaccheo.com/home.php')
        xuNow = self.getXu.text.split('id="soduchinh"')[1].split('</strong>')[0].split(">")[1]
        return xuNow
    def dat_nick(self, uid, loai):
        data = {
            "iddat[]": uid,
            "loai": loai
        }
        self.dat = self.s.post('https://tuongtaccheo.com/cauhinh/datnick.php', data=data, timeout=10)
        return self.dat.text
username = 'hayashibutler'    
password = '654321'
ttc = login(username=username, password=password)
print(ttc.get_cookies())

# get xu
xu = ttc.check_xu()
print(xu)

# dat nick
uid = '100065492352370'
# uid = '100090496562154'
loai = 'fb'
dat = ttc.dat_nick(uid, loai)
print(dat)