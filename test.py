import requests
import urllib.request
from bs4 import BeautifulSoup
from hdr import header_chrome
from getpass import getpass

session = requests.Session()

url = 'https://www.dcinside.com/'
loginUrl = 'http://dcid.dcinside.com/join/member_check.php'
s = session.get(url, headers=header_chrome)

print(s.cookies.get_dict())
soup = BeautifulSoup(s.text, "html.parser")

param = {
    'user_id': 'testeract',
    'password': 'test1234',
    's_url': '//www.dcinside.com/',
    'ssl': 'Y',
    '9K4CAexSSc7ur1Ty': '93318AC0B0Xo4991',
    'id_cookie': 'N'
}
# param['user_id'] = input("id:\n>>>")
# param['password'] = getpass()
# s = session.post(loginUrl, data=param, headers=header_login)
print(s.cookies.get_dict())

# s = session.get(url, cookies=s.cookies, headers=header_chrome)
# print(r.text)
soup = BeautifulSoup(s.text, "html.parser")
try:
    hey = soup.find("div", {"class": "box_user"}).get_text()
except Exception:
    hey = soup.find("strong", {"class": "fc_2b"}).get_text()
    print("logged-in")
else:
    print("NOT logged-in")
# print('----------------------------')
# print(s.text)
with open("result.txt", "wt") as f:
    f.write(s.text)
