import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'referer': 'https://www.immoweb.be/en'
}

request = session.get("https://www.immoweb.be/en/classified/house/for-sale/bertrix/6880/10161791", headers=headers)
with open("rew_test.txt","w+",encoding="utf-8") as log:
    print(request.text,file=log)

