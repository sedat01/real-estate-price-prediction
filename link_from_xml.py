from gettext import find
import xml
from bs4 import BeautifulSoup
import requests


with open("links.txt","w+",encoding="utf-8") as f:
    pass

property_type = "/apartment/for-sale/"
s = requests.Session()

sitemap = s.get("https://www.immoweb.be/sitemap.xml")
sitemap = sitemap.content
sitemap = BeautifulSoup(sitemap,"xml")
sitemap = sitemap.find_all("loc")
sitemap_url_list = []
for url in range(len(sitemap)):
    if "classifieds" in sitemap[url].text:
        sitemap_url_list.append(sitemap[url].text)

i = 0
        
for url in sitemap_url_list:
    i+=1
    print(f"URL {i}")
    data = s.get(url)
    data = data.content
    soup = BeautifulSoup(data, "xml")
    urls = soup.find_all("url")
    with open("links.txt","a",encoding="utf-8") as f:
        for url in range(len(urls)):
            if "/en/" in urls[url].find("loc").text and property_type in urls[url].find("loc").text :
                print(urls[url].find("loc").text,file=f)